#!/bin/sh

# usage info
usage()
{
cat << EOF
usage: $0 options passthrough-args

Iceprod core framework starter script.

OPTIONS:
 -h        Show this message
 -d <arg>  Download URL
 -c <arg>  Cache/proxy for http
 -s <arg>  IceProd software location
 -m <arg>  Platform
 -u <arg>  Download Username
 -p <arg>  Download Password
 -e <arg>  env filename
 -x <arg>  x509 proxy filename

EOF
}

# get args
INC=0
while getopts ":hd:c:s:m:u:p:e:x:" opt; do
    case $opt in
        h)
            usage
            exit
            ;;
        d)
            DOWNLOAD_URL=$OPTARG
            ;;
        c)
            PROXY=$OPTARG
            ;;
        s)
            SROOT=$OPTARG
            ;;
        m)
            PLATFORM=$OPTARG
            ;;
        u)
            USERNAME=$OPTARG
            ;;
        p)
            PASSWORD=$OPTARG
            ;;
        e)
            ENV=$OPTARG
            ;;
        x)
            X509=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            echo "Option parsing halted early."
            echo "Passing all other arguments on to i3exec.py"
            break
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
    INC=$((INC+2))
done
shift $INC
echo " "

# calculate platform
OSTYPE=`uname`
if [ $OSTYPE = 'Linux' ]; then
    VER=`ldd --version|awk 'NR>1{exit};{print $(NF)}'`
    HASH=hash
else
    VER=`uname -r`
    HASH=type
fi
if [ -z $PLATFORM ]; then
    ARCH=`uname -m | sed -e 's/Power Macintosh/ppc/ ; s/i686/i386/'`
    UNICODEVERSION=`python -c "import sys;sys.stdout.write('ucs4') if sys.maxunicode == 1114111 else sys.stdout.write('ucs2')"`
    if [ ! "$?" = "0" ]; then
        unicodeversion='ucs4'
    fi
    PLATFORM="$ARCH.$OSTYPE.$VER.$UNICODEVERSION"
fi
echo "Platform: $PLATFORM"
export PLATFORM

if [ -z $SROOT ]; then
    SROOT="/cvmfs/icecube.opensciencegrid.org/iceprod"
fi
if [ -z $PROXY ]; then
    PROXY="cache01.hep.wisc.edu:80"
fi

PYBIN=python
if [ -d $PWD/iceprod ]; then
    # local iceprod available, assume env is good
    # (this is mostly for testing)
    if [ -z $PYTHONPATH ]; then
        export PYTHONPATH=$PWD:$PYTHONPATH
    else
        export PYTHONPATH=$PWD
    fi
else
    if [ ! -d $SROOT ]; then
        # first, try parrot
        TEST_PARROT="parrot_run -p $PROXY ls $SROOT"
        if ( $HASH parrot_run ) && $TEST_PARROT >/dev/null 2>/dev/null; then
            PYBIN="parrot_run -p $PROXY $SROOT/setup.sh python"
        else
            # try tarball

            # test DOWNLOAD_URL
            if [ -z $DOWNLOAD_URL ]; then
                echo "Download URL required" >&2
                exit 1
            fi
            # Download env for this platform
            if [ -z $ENV ]; then
                ENV="env.$PLATFORM.tar.gz"
            fi
            ENV_URL="$DOWNLOAD_URL/lib/$ENV"
            if [ ! -f $ENV ]; then
                # test for curl, wget, and fetch
                if ( $HASH curl >&- 2>&- ); then
                    if [ ! -z $USERNAME ] && [ ! -z $PASSWORD ]; then
                        if ! ( curl --retry 5 --max-time 30 -f -u $USERNAME:$PASSWORD -o $ENV $ENV_URL ); then
                            echo "failed to download $ENV_URL"
                            exit 1
                        fi
                    else
                        if ! ( curl --retry 5 --max-time 30 -f -o $ENV $ENV_URL ); then
                            echo "failed to download $ENV_URL"
                            exit 1
                        fi
                    fi
                elif ( $HASH wget >&- 2>&- ); then
                    if [ ! -z $USERNAME ] && [ ! -z $PASSWORD ]; then
                        if ! ( wget -r --tries=5 --timeout=30 --user=$USERNAME --password=$PASSWORD -O $ENV $ENV_URL ); then
                            echo "failed to download $ENV_URL"
                            exit 1
                        fi
                    else
                        if ! ( wget -r --tries=5 --timeout=30 -O $ENV $ENV_URL ); then
                            echo "failed to download $ENV_URL"
                            exit 1
                        fi
                    fi
                elif ( $HASH fetch >&- 2>&- ); then
                    if [ ! -z $USERNAME ] && [ ! -z $PASSWORD ]; then
                        echo "Fetch does not support USERNAME and PASSWORD.  Trying without..."
                    fi
                    if ! ( fetch -a -T 30 -o $ENV $ENV_URL ); then
                        echo "failed to download $ENV_URL"
                        exit 1
                    fi
                else
                    echo "Can't find wget, curl, or fetch.  At least one is required"
                    exit 1
                fi
            fi
            # extract env
            ENVEND=$(echo $ENV | awk  '{print substr($0, length($0) - 2, length($0))}')
            if [ "$ENVEND" = ".gz" ]; then
                if ! ( tar -zxf $ENV ); then
                    echo "Failed to extract $ENV"
                    exit 1
                fi
            elif [ "$ENVEND" = "bz2" ]; then
                if ! ( tar -jxf $ENV ); then
                    echo "Failed to extract $ENV"
                    exit 1
                fi
            elif [ "$ENVEND" = ".xz" ]; then
                if ! ( tar -Jxf $ENV ); then
                    echo "Failed to extract $ENV"
                    exit 1
                fi
            ENVEND=$(echo $ENV | awk  '{print substr($0, length($0) - 3, length($0))}')
            elif [ "$ENVEND" = "lzma" ]; then
                if ! ( tar --lzma -xf $ENV ); then
                    echo "Failed to extract $ENV"
                    exit 1
                fi
            elif [ "$ENVEND" = ".tar" ]; then
                if ! ( tar -xf $ENV ); then
                    echo "Failed to extract $ENV"
                    exit 1
                fi
            else
                echo "Unknown extension for $ENV"
                exit 1
            fi

            # check env extraction
            if [ ! -d $PWD/env ] || [ ! -d $PWD/env/bin ]; then
                echo "Something is wrong with the env directory structure"
                exit 1
            fi

            # set python location
            PYBIN=$PWD/env/bin/python

            # set rest of environment
            export PATH=$PWD/env/bin:$PATH
            export LD_LIBRARY_PATH=$PWD/env/lib:$PWD/env/lib64:$LD_LIBRARY_PATH
            export DYLD_LIBRARY_PATH=$PWD/env/lib:$PWD/env/lib64:$DYLD_LIBRARY_PATH
            export PYTHONPATH=$PWD/env/lib/python`python -c 'import sys;print(".".join([str(x) for x in sys.version_info[:2]]))'`/site-packages:$PWD/env/lib:$PYTHONPATH
        fi
    else
        echo "Using software at $SROOT"
        if [ -f $SROOT/setup.sh ]; then
            eval `$SROOT/setup.sh`
        else
            export PATH=$SROOT/bin:$PATH
            export LD_LIBRARY_PATH=$SROOT/lib:$SROOT/lib64:$LD_LIBRARY_PATH
            export DYLD_LIBRARY_PATH=$SROOT/lib:$SROOT/lib64:$DYLD_LIBRARY_PATH
            export PYTHONPATH=$SROOT/lib/python`python -c 'import sys;print(".".join([str(x) for x in sys.version_info[:2]]))'`/site-packages:$SROOT/lib:$PYTHONPATH
        fi
    fi
fi

# create resource_libs directory
if [ ! -d $PWD/resource_libs ]; then
    mkdir resource_libs
fi
export LD_LIBRARY_PATH=$PWD/resource_libs:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$PWD/resource_libs:$DYLD_LIBRARY_PATH

# set proxy
if [ ! -z $X509 ]; then
    export X509_USER_PROXY=$PWD/$X509
elif [ -z $X509_USER_PROXY ]; then
    export X509_USER_PROXY=$PWD/x509up
fi

# run i3exec
if [ -z $DOWNLOAD_URL ]; then
    cmd="$PYBIN -m iceprod.core.i3exec --offline $@"
else
    cmd="$PYBIN -m iceprod.core.i3exec --url=$DOWNLOAD_URL $@"
fi
echo $cmd
exec $cmd

# clean up after ourselves
rm -Rf resource_libs $ENV env
