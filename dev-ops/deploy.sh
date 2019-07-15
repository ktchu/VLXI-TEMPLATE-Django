#!/bin/bash

#-----------------------------------------------------------------------------
# Helper Functions
#-----------------------------------------------------------------------------

function usage()
{
    script_name=`basename $0`

    echo "
NAME
    $script_name -- set up Django web application

SYNOPSIS
    $script_name [-h] [-v] [-c] [-R] CONFIG_FILE

DESCRIPTION
    The $script_name script sets up the Django web application (e.g. set
    up database).

    Notes:
    - This script assumes that all Django databases are stored using the same
      type of database backend.

CONFIGURATION FILE PARAMETERS

    - apache

      * server_name : fully-qualified domain name of web server

      * server_admin : email address that should be included in any error
                       messages shown to the user.

    - aws

      * ami_type : AMI type

    - data

      * load_test_data : flag indicating whether or not to load test data
                         into database. Valid values: yes, no, true, false.
                         Default: false.

    - django

      * project_name : name of Django project

      * settings_module : Django settings module (Python dot notation)

ARGUMENTS

    CONFIG_FILE
        configuration file to use for setup

OPTIONS
    -c
        create database.
        Default: database not created.

    -R
        reset database.  Existing database is dropped.  Implies '-c'.
        Default: database not reset.

    -v
        enable verbose mode.
        Default: verbose mode disabled.

    -h
        print help message

REQUIREMENTS
    * bash_ini_parser

AUTHORS
    Kevin Chu
"
}


#-----------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------

# Status codes
_EXIT_CODE_SUCCESS=0
_EXIT_CODE_CMD_OPT_ERR=1
_EXIT_CODE_ERR_MMISSING_CONFIG_FILE_ARG=2
_EXIT_CODE_CONFIG_FILE_NOT_FOUND=3
_EXIT_CODE_CONFIG_FILE_ERR_NO_APACHE_SERVER_NAME=4
_EXIT_CODE_CONFIG_FILE_ERR_NO_APACHE_SERVER_ADMIN=5
_EXIT_CODE_CONFIG_FILE_ERR_NO_AWS_AMI_TYPE=6
_EXIT_CODE_CONFIG_FILE_ERR_NO_DJANGO_PROJECT_NAME=7
_EXIT_CODE_CONFIG_FILE_ERR_UNKNOWN_AWS_AMI_TYPE=8
_EXIT_CODE_CONFIG_FILE_ERR_NO_PYTHON_VERSION=9
_EXIT_CODE_DJANGO_SETTINGS_ERR_NO_DB_ENGINE=10
_EXIT_CODE_DJANGO_SETTINGS_ERR_NO_DB_NAME=11
_EXIT_CODE_DJANGO_SETTINGS_ERR_NO_DB_USER=12
_EXIT_CODE_DJANGO_SETTINGS_ERR_NO_DB_PASSWORD=13
_EXIT_CODE_DJANGO_SETTINGS_ERR_UNKNOWN_DB_ENGINE=14
_EXIT_CODE_POSTGRESQL_ERR_NO_AUTOMATIC_DB_RESET=15
_EXIT_CODE_POSTGRESQL_ERR_NO_AUTOMATIC_DB_CREATION=16

#-----------------------------------------------------------------------------
# Process command-line
#-----------------------------------------------------------------------------

# Default option parameters
verbose_mode=false
create_database=false
reset_database=false

# Process options
options=":AcvhR"
optind=1
while getopts "$options" opt; do
    case $opt in
        c)
            create_database=true
            ;;
        R)
            reset_database=true
            create_database=true
            ;;
        v)
            verbose_mode=true
            ;;
        h)
            usage
            exit $_EXIT_CODE_SUCCESS
            ;;
        \?)
            usage
            exit $_EXIT_CODE_CMD_OPT_ERR
            ;;
        \:)
            echo "Option -$optarg requires an argument." >&2
            usage
            exit $_EXIT_CODE_CMD_OPT_ERR
            ;;
    esac
done

# Process arguments
shift $((optind-1))
if [ $# -lt 1 ]; then
    echo "ERROR: CONFIG_FILE argument missing."
    usage
    exit $_EXIT_CODE_ERR_MMISSING_CONFIG_FILE_ARG
fi
if [ $# -gt 1 ]; then
    echo "WARNING: more than arguments found.  Ignoring all but first one."
fi
config_file=$1

# Check command-line arguments
if [ ! -z "$config_file" ]; then
    if [ ! -f "$config_file" ]; then
        echo "ERROR: CONFIG_FILE '$config_file' not found."
        exit $_EXIT_CODE_CONFIG_FILE_NOT_FOUND
    fi
fi


#-----------------------------------------------------------------------------
# General Preparations
#-----------------------------------------------------------------------------

# Find top-level data-loader directory
dev_ops_top_dir=$(cd `dirname ${BASH_SOURCE[0]}`; pwd)

# Set PATH
export PATH="$dev_ops_top_dir/bin:$PATH"

# Django project structure
apps_dir=apps

# Change to the top directory
cd $dev_ops_top_dir


#-----------------------------------------------------------------------------
# Read configuration file
#-----------------------------------------------------------------------------

# --- Load parameter values from configuration file

bash_lib_path=$dev_ops_top_dir/lib
if [ ! -z "$config_file" ]; then
    source $bash_lib_path/bash_ini_parser/read_ini.sh
    read_ini $config_file
fi

# --- Apache configuration

# Set server_name and server_admin
if [ ! -z "$INI__apache__server_name" ]; then
    server_name=$INI__apache__server_name
else
    echo "ERROR: 'apache.server_name' not set in config file."
    exit $_EXIT_CODE_CONFIG_FILE_ERR_NO_APACHE_SERVER_NAME
fi

if [ ! -z "$INI__apache__server_admin" ]; then
    server_admin=$INI__apache__server_admin
else
    server_admin=admin@example.com
    echo "ERROR: 'apache.server_admin' not set in config file."
    exit $_EXIT_CODE_CONFIG_FILE_ERR_NO_APACHE_SERVER_ADMIN
fi

# --- AWS configuration

# Set ami_type
if [ ! -z "$INI__aws__ami_type" ]; then
    ami_type=$INI__aws__ami_type
else
    echo "ERROR: 'aws.ami_type' not set in config file."
    exit $_EXIT_CODE_CONFIG_FILE_ERR_NO_AWS_AMI_TYPE
fi
if [ "$ami_type" != "amazon-linux" -a "$ami_type" != "ubuntu" ]; then
    echo "ERROR: unknown AMI type '$ami_type'"
    exit $_EXIT_CODE_CONFIG_FILE_ERR_UNKNOWN_AWS_AMI_TYPE
fi

# --- Django configuration

# Set django_project_name
if [ ! -z "$INI__django__project_name" ]; then
    django_project_name=$INI__django__project_name
else
    echo "ERROR: 'django.project_name' not set in config file."
    exit $_EXIT_CODE_CONFIG_FILE_ERR_NO_DJANGO_PROJECT_NAME
fi
django_project_home=$(cd $dev_ops_top_dir/..; pwd)
export PATH="$django_project_home/bin:$PATH"

# Set DJANGO_SETTINGS_MODULE
if [ ! -z "$INI__django__settings_module" ]; then
    DJANGO_SETTINGS_MODULE=$INI__django__settings_module
else
    DJANGO_SETTINGS_MODULE="$django_project_name.settings"
fi
export DJANGO_SETTINGS_MODULE
bare_settings_module="${DJANGO_SETTINGS_MODULE##*.}"
django_settings_file="$django_project_home/$django_project_name/$bare_settings_module.py"

# --- Miscellaneous configuration

# Set load_test_data
load_test_data=false # default value
if [ ! -z "$INI__misc__load_test_data" ]; then
    if [ $INI__misc__load_test_data = "1" ]; then
        load_test_data=true
    fi
fi

# Set Python version
if [ ! -z "$INI__misc__python_version" ]; then
    python_version_raw=$INI__misc__python_version
    python_version_major=`echo $python_version_raw | cut -d . -f 1`
    python_version_minor=`echo $python_version_raw | cut -d . -f 2`
    python_version="$python_version_major.$python_version_minor"
else
    echo "ERROR: 'misc.python_version' not set in config file."
    exit $_EXIT_CODE_CONFIG_FILE_ERR_NO_PYTHON_VERSION
fi

#-----------------------------------------------------------------------------
# Django Setup
#-----------------------------------------------------------------------------

# --- Preparations

# Change to top-level Django project directory
pushd $django_project_home > /dev/null

# --- Django Preparations

# Set environment variables
export PYTHONPATH="$django_project_home:$PYTHONPATH"

# --- Get database properties

# Database engines
db_engines=`grep ENGINE $django_settings_file | \
            cut -d : -f 2 | cut -d , -f 1 | sed "s/[\"' ]//g"`
if [ -z "$db_engines" ]; then
    echo "ERROR: 'ENGINE' not found in Django settings file."
    exit $_EXIT_CODE_DJANGO_SETTINGS_ERR_NO_DB_ENGINE
fi
read -a db_engines <<< $db_engines
for index in "${!db_engines[@]}"; do
    db_engine=${db_engines[$index]}
    db_engine="${db_engine##*.}"
    db_engines[$index]=$db_engine
done

# Database names
base_dir=$(dirname "${BASH_SOURCE[0]}")
db_names_with_base_dir_raw=`\
    grep NAME $django_settings_file | grep -v 'django.contrib.auth' | \
    grep BASE_DIR | \
    cut -d : -f 2 | cut -d , -f 2 | sed "s/)//g" | sed "s/[\"' ]//g"`
db_names_with_base_dir=""
for db_name in $db_names_with_base_dir_raw; do
    db_names_with_base_dir="$db_names_with_base_dir $base_dir/$db_name"
done
db_names_without_base_dir=`
    grep NAME $django_settings_file | grep -v 'django.contrib.auth' | \
    grep -v BASE_DIR | \
    cut -d : -f 2 | cut -d , -f 1 | sed "s/[\"' ]//g"`
db_names="$db_names_with_base_dir $db_names_without_base_dir"
if [ -z "$db_names" ]; then
    echo "ERROR: 'NAME' not found in Django settings file."
    exit $_EXIT_CODE_DJANGO_SETTINGS_ERR_NO_DB_NAME
fi
read -a db_names <<< $db_names
for index in "${!db_names[@]}"; do
    db_names[$index]=${db_names[$index]}
done

# Database hosts, ports, users and passwords
if [ "$db_engine" != "sqlite3" ]; then
    db_users=`grep USER $django_settings_file | \
                cut -d : -f 2 | cut -d , -f 1 | sed "s/[\"' ]//g"`
    if [ -z "$db_users" ]; then
        echo "ERROR: 'USER' not found in Django settings file."
        exit $_EXIT_CODE_DJANGO_SETTINGS_ERR_NO_DB_USER
    fi
    read -a db_users <<< $db_users
    for index in "${!db_users[@]}"; do
        db_users[$index]=${db_users[$index]}
    done

    db_passwords=`grep PASSWORD $django_settings_file | \
                cut -d : -f 2 | cut -d , -f 1 | sed "s/[\"' ]//g"`
    if [ -z "$db_passwords" ]; then
        echo "ERROR: 'PASSWORD' not found in Django settings file."
        exit $_EXIT_CODE_DJANGO_SETTINGS_ERR_NO_DB_PASSWORD
    fi
    read -a db_passwords <<< $db_passwords
    for index in "${!db_passwords[@]}"; do
        db_passwords[$index]=${db_passwords[$index]}
    done

    db_hosts=`grep HOST $django_settings_file | grep -v ALLOWED_HOSTS | \
                cut -d : -f 2 | cut -d , -f 1 | sed "s/[\"' ]//g"`
    if [ -z "$db_hosts" ]; then
        db_host='localhost'
        for index in "${!db_passwords[@]}"; do
            db_hosts[$index]=$db_host
        done

        echo "INFO: 'HOST' not found in Django settings file.  Using '$db_host'."
    else
        read -a db_hosts <<< $db_hosts
        for index in "${!db_hosts[@]}"; do
            db_hosts[$index]=${db_hosts[$index]}
        done
    fi

    db_port=`grep PORT $django_settings_file | \
                cut -d : -f 2 | cut -d , -f 1 | sed "s/[\"' ]//g"`
    if [ -z "$db_port" ]; then
        for index in "${!db_passwords[@]}"; do
            db_name=${db_names[$index]}
            db_engine=${db_engines[$index]}

            if [ "$db_engine" = "mysql" ]; then
                db_port=3306
                echo "INFO: 'PORT' not found in Django settings file.  Using default port $db_port for $db_engine backend."
            elif [ "$db_engine" = "postgresql_psycopg2" ]; then
                db_port=5432
                echo "INFO: 'PORT' not found in Django settings file.  Using default port $db_port for $db_engine backend."
            else
                echo "INFO: Unknown database engine for $db_name"
                exit $_EXIT_CODE_DJANGO_SETTINGS_ERR_UNKNOWN_DB_ENGINE
            fi

            db_ports[$index]=$db_port
        done
    else
        read -a db_ports <<< $db_ports
        for index in "${!db_ports[@]}"; do
            db_ports[$index]=${db_ports[$index]}
        done
    fi
fi

# Change back to original directory
popd > /dev/null

#-----------------------------------------------------------------------------
# Database Setup
#-----------------------------------------------------------------------------

# --- Preparations

# Change to top-level Django project directory
pushd $django_project_home > /dev/null

# --- Drop database

if $reset_database; then

    for index in "${!db_names[@]}"; do

        db_name=${db_names[$index]}
        db_engine=${db_engines[$index]}

        echo
        echo "Dropping database '$db_name'..."

        if [ "$db_engine" = "sqlite3" ]; then
            if [ -f $db_name ]; then
                echo
                echo "$db_name already exists.  It will be overwritten."
                echo -n "Are you sure you want to proceed (y/N)?"
                read USER_RESPONSE

                if [ "$USER_RESPONSE" = "y" -o "$USER_RESPONSE" = "Y" ]; then
                    rm -f $db_name
                else
                    echo
                    echo "Exiting without modifying $db_name."
                    exit $_EXIT_CODE_SUCCESS
                fi
            fi

        elif [ "$db_engine" = "mysql" ]; then
            db_host=${db_hosts[$index]}
            db_port=${db_ports[$index]}
            db_user=${db_users[$index]}
            db_password=${db_passwords[$index]}

            # Drop database
            echo "DROP DATABASE IF EXISTS $db_name;" | \
            mysql --host=$db_host --port=$db_port \
                  --user=$db_user --password=$db_password

        elif [ "$db_engine" = "postgresql_psycopg2" ]; then
            echo "Automatic database reset not supported when using"
            echo "PostgreSQL backend.  Please set up database manually and"
            echo "then re-run deploy.sh"

            exit $_EXIT_CODE_POSTGRESQL_ERR_NO_AUTOMATIC_DB_RESET

        fi
    done
fi

# --- Create database

if $create_database; then

    for index in "${!db_names[@]}"; do

        db_name=${db_names[$index]}
        db_engine=${db_engines[$index]}

        echo
        echo "Creating database '$db_name'..."

        if [ "$db_engine" = "mysql" ]; then
            db_host=${db_hosts[$index]}
            db_port=${db_ports[$index]}
            db_user=${db_users[$index]}
            db_password=${db_passwords[$index]}

            # Create database
            echo "CREATE DATABASE IF NOT EXISTS $db_name;" | \
            mysql --host=$db_host --port=$db_port \
                  --user=$db_user --password=$db_password

        elif [ "$db_engine" = "postgresql_psycopg2" ]; then
            echo "Automatic database creation not supported when using"
            echo "PostgreSQL backend.  Please set up database manually and"
            echo "then re-run deploy.sh"

            exit $_EXIT_CODE_POSTGRESQL_ERR_NO_AUTOMATIC_DB_CREATION

        fi
    done
fi

# --- Update database tables

echo
echo "Updating database tables..."

python manage.py migrate

# --- Change back to original directory

popd > /dev/null

#-----------------------------------------------------------------------------
# Load data
#-----------------------------------------------------------------------------

# --- Load test data into database

# Change to top-level Django project directory
pushd $django_project_home > /dev/null

if $load_test_data; then
    echo
    echo "Loading test data ... NOT YET IMPLEMENTED"
    #python manage.py loaddata test_data.json

fi

# Change back to original directory
popd > /dev/null

#-----------------------------------------------------------------------------
# Apache configuration
#-----------------------------------------------------------------------------

echo -n "Generating Apache configuration files..."

# --- Preparations

# Set username for EC2 user
if [ "$ami_type" = "amazon-linux" ]; then
    ec2_user=ec2-user
elif [ "$ami_type" = "ubuntu" ]; then
    ec2_user=ubuntu
fi

# Construct directory paths for Apache configuration templates and files
apache_conf_template_dir_prefix=$(cd $dev_ops_top_dir/templates/apache2/$ami_type; pwd)
apache_conf_dir_prefix=$dev_ops_top_dir/conf/apache2

if [ "$ami_type" = "amazon-linux" ]; then
    apache_conf_template_dir=$apache_conf_template_dir_prefix/conf.d
    apache_conf_dir=$apache_conf_dir_prefix/conf.d
elif [ "$ami_type" = "ubuntu" ]; then
    apache_conf_template_dir=$apache_conf_template_dir_prefix/sites-available
    apache_conf_dir=$apache_conf_dir_prefix/sites-available
fi

# Create directory for generated Apache configuration files
if [ -d $apache_conf_dir ]; then
    rm -rf $apache_conf_dir
fi
mkdir -p $apache_conf_dir

# --- Apache site configuration files

# Set virtual environment directory
virtualenv_home=/home/$ec2_user/.virtualenvs/$django_project_name

# Construct configuration file list
template_files=`ls $apache_conf_template_dir/*.template`
conf_files=""
for template_file in $template_files; do
    conf_files="$conf_files `basename ${template_file%.*}`"
done

# Generate configuration files from templates
for conf_file in $conf_files; do
    template_file_path=$apache_conf_template_dir/$conf_file.template
    conf_file_path=$apache_conf_dir/$conf_file

    cat $template_file_path \
        | sed -e "s|{{[[:space:]]*SERVER_NAME[[:space:]]*}}|$server_name|g" \
        > $conf_file_path

    cat $conf_file_path \
        | sed -e "s|{{[[:space:]]*SERVER_ADMIN[[:space:]]*}}|$server_admin|g" \
        > $conf_file_path.1
    mv -f $conf_file_path.1 $conf_file_path

    cat $conf_file_path \
        | sed -e "s|{{[[:space:]]*DJANGO_PROJECT_HOME[[:space:]]*}}|$django_project_home|g" \
        > $conf_file_path.1
    mv -f $conf_file_path.1 $conf_file_path

    cat $conf_file_path \
        | sed -e "s|{{[[:space:]]*DJANGO_PROJECT_NAME[[:space:]]*}}|$django_project_name|g" \
        > $conf_file_path.1
    mv -f $conf_file_path.1 $conf_file_path

    cat $conf_file_path \
        | sed -e "s|{{[[:space:]]*VIRTUALENV_HOME[[:space:]]*}}|$virtualenv_home|g" \
        > $conf_file_path.1
    mv -f $conf_file_path.1 $conf_file_path

done

echo "done"

#-----------------------------------------------------------------------------
# Epilogue
#-----------------------------------------------------------------------------

echo "
============================================================================

MANUAL DEPLOYMENT STEPS
-----------------------"

# Apache deployment
if [ "$ami_type" = "amazon-linux" ]; then
    apache_user=apache
    httpd_service=httpd
elif [ "$ami_type" = "ubuntu" ]; then
    apache_user=www-data
    httpd_service=apache2
fi
virtualenv_top_dir=`dirname $virtualenv_home`

echo "
* Deploy Apache configuration files."

if [ "$ami_type" = "amazon-linux" ]; then

    echo "
  - Remove the following files from /etc/httpd/conf.d

    * autoindex.conf
    * userdir.conf
    * ssl.conf

  - Install Apache configuration files located in dev-ops/apache2/conf to
    /etc/httpd.

    $ cd $django_project_home
    $ sudo cp -f dev-ops/conf/apache2/conf.d/*.conf /etc/httpd/conf.d/"

elif [ "$ami_type" = "ubuntu" ]; then

    echo "
  - Install Apache configuration files located in dev-ops/apache2/conf to
    /etc/apache2.

    $ cd $django_project_home
    $ sudo cp -f dev-ops/conf/apache2/sites-available/*.conf /etc/apache2/sites-available/

  - Disable default site and enable $django_project_name site.

    $ sudo a2dissite 000-default
    $ sudo a2ensite $django_project_name"
fi

echo "
  - Set permissions for /home/$ec2_user directory.

    * Secure contents of /home/$ec2_user directory.

      $ chmod -R og-rwx /home/$ec2_user

    * Grant group read-only access to directories required for web
      application.

      # '$ec2_user' home directory
      $ chmod g+x /home/$ec2_user

      # Django project directory
      $ chmod -R g+r $django_project_home
      $ find $django_project_home -type d -exec chmod g+x {} \;

      # Virtual environment directory
      $ chmod g+x $virtualenv_top_dir
      $ chmod -R g+r $virtualenv_home
      $ find $virtualenv_home -type d -exec chmod g+x {} \;

  - Change group to '$apache_user' for directories required for web application.

      $ sudo chgrp $apache_user /home/$ec2_user
      $ sudo chgrp -R $apache_user $django_project_home
      $ sudo chgrp $apache_user $virtualenv_top_dir
      $ sudo chgrp -R $apache_user $virtualenv_home

  - Restart Apache.

    $ sudo service $httpd_service restart"

# Django
echo "
* Set up symbolic links to make Django static files available Apache.

  - Django admin site static files

    $ cd $django_project_home/static
    $ ln -s $virtualenv_home/lib/python$python_version/site-packages/django/contrib/admin/static/admin admin

  - Django REST Framework static files

    $ cd $django_project_home/static
    $ ln -s $virtualenv_home/lib/python$python_version/site-packages/rest_framework/static/rest_framework rest_framework"

# Demo data
echo "
* (OPTIONAL) Load demo data.

  - Use the scripts in the 'demo' directory.

    $ cd demo
    $ python load-demo-data.py data"

# SQLite
if [ "$db_engine" = "sqlite3" ]; then
    echo "
* Set the permissions on the SQLite database file.
  "

    for index in "${!db_names[@]}"; do
        db_name=`echo ${db_names[$index]} | cut -d '/' -f 2;`
        echo "  $ sudo chgrp $apache_user $django_project_home/$db_name"
        echo "  $ chmod g+rw $django_project_home/$db_name"
    done
fi

echo "
============================================================================
"
