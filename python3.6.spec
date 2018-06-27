%define docver 3.6.5
%define dirver 3.6

%define _disable_lto 1

%define api %{dirver}
%define major 1
%define libname %mklibname python %{api}m %{major}
%define devname %mklibname python3.6 -d

%ifarch %{ix86} x86_64 ppc
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

%define __python_provides %{nil}
%define __python_requires %{nil}

# weird stuff
# pip not available if python package built with pip
# * build without pip files lead to good package
# * but next package lead to unpackaged pip files 
# let's disable pip
%bcond_with pip
%bcond_without abi_m

Summary:	An interpreted, interactive object-oriented programming language
Name:		python3.6
Version:	3.6.5
Release:	2
License:	Modified CNRI Open Source License
Group:		Development/Python
Url:		http://www.python.org/
Source0:	http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source1:	http://www.python.org/ftp/python/doc/%{docver}/python-%{docver}-docs-html.tar.bz2
Source2:	python3.6.macros
Source3:	pybytecompile.macros
Source100:	%{name}.rpmlintrc
#Source4:	python-mode-1.0.tar.bz2
Patch0:		python-3.6.1-module-linkage.patch
Patch1:		http://pkgs.fedoraproject.org/cgit/rpms/python3.git/plain/00102-lib64.patch
Patch2:		http://pkgs.fedoraproject.org/cgit/rpms/python3.git/plain/00104-lib64-fix-for-test_install.patch
Patch3:		Python-select-requires-libm.patch
Patch4:		python-3.3.0b1-test-posix_fadvise.patch
Patch6:		python-3.6.2-clang-5.0.patch
Patch7:		http://pkgs.fedoraproject.org/cgit/rpms/python3.git/plain/00205-make-libpl-respect-lib64.patch
# 00173 #
# Workaround for ENOPROTOOPT seen in bs within
# test.test_support.bind_port()
# from Fedora (rhbz#913732)
Patch173:	00173-workaround-ENOPROTOOPT-in-bind_port.patch
Patch179:	00179-dont-raise-error-on-gdb-corrupted-frames-in-backtrace.patch
Patch181:	http://pkgs.fedoraproject.org/cgit/rpms/python3.git/plain/00157-uid-gid-overflows.patch
Patch183:	00178-dont-duplicate-flags-in-sysconfig.patch
Patch184:	00201-fix-memory-leak-in-gdbm.patch

BuildRequires:	blt
BuildRequires:	bzip2-devel
BuildRequires:	db-devel
BuildRequires:	gdbm-devel
BuildRequires:	gmp-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libffi) >= 3.1
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	python2
%if %{with valgrind}
BuildRequires:	valgrind-devel
%endif
BuildConflicts:	python-pyxml
Provides:	/usr/bin/python%{dirver}mu
Conflicts:	%{libname}-devel < 3.1.2-4
Conflicts:	%{devname} < 3.2.2-3
Conflicts:	python-pyxml

%if %{with pip}
%rename	python-setuptools
%rename	python-pkg-resources
Provides:	python3egg(setuptools)
Provides:	python3egg(distribute)
%endif

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that
need a programmable interface. This package contains most of the
standard Python modules, as well as modules for interfacing to the
Tix widget set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%package -n %{libname}
Summary:	Shared libraries for Python %{version}
Group:		System/Libraries

%description -n	%{libname}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.

%package -n %{devname}
Summary:	The libraries and header files needed for Python development
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install %{devname} if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package docs
Summary:	Documentation for the Python programming language
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	xdg-utils
BuildArch:	noarch

%description docs
The python-docs package contains documentation on the Python
programming language and interpreter.  The documentation is provided
in ASCII text files and in LaTeX source files.

Install the python-docs package if you'd like to use the documentation
for the Python language.

%package -n tkinter3.6
Summary:	A graphical user interface for the Python scripting language
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	tcl
Requires:	tk

%description -n	tkinter3.6
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package -n tkinter3.6-apps
Summary:	Various applications written using tkinter
Group:		Development/Python
Requires:	tkinter3.6 = %{EVRD}

%description -n	tkinter3.6-apps
Various applications written using tkinter.

%prep
%setup -qn Python-%{version}
%patch0 -p1 -b .link~

%if "%{_lib}" == "lib64"
%patch1 -p1 -b .lib64~
%patch2 -p1 -b .p2~
%endif
%patch3 -p1 -b .lm~
%patch4 -p1 -b .p4~
%patch6 -p1 -b .clang5~
%patch7 -p1 -b .libpl
%patch173 -p1 -b .p173~
%patch179 -p1 -b .p179~
%patch181 -p1
%patch183 -p1
%patch184 -p1

# docs
mkdir html
tar xf %{SOURCE1} -C html

find . -type f -print0 | xargs -0 sed -i -e 's@/usr/local/bin/python@%{_bindir}/python@'

cat > README.omv << EOF
Python interpreter support readline completion by default.
This is only used with the interpreter. In order to remove it,
you can :
1) unset PYTHONSTARTUP when you login
2) create a empty file \$HOME/.pythonrc.py
3) change %{_sysconfdir}/pythonrc.py
EOF

#   Remove embedded copy of libffi:
for SUBDIR in darwin libffi_msvc libffi_osx ; do
  rm -r Modules/_ctypes/$SUBDIR || exit 1 ;
done

# Ensure that internal copies of expat, libffi and zlib are not used.
rm -fr Modules/expat
rm -fr Modules/zlib

%build
%global optflags %{optflags} -O3

rm -f Modules/Setup.local

# fedya
# if you drop ABIFLAGS
# you got libpython-3.4-1.0.so lib
# instead of libpython-3.4m-1.0.so lib
%if !%{with abi_m}
sed -e "s/ABIFLAGS=\"\${ABIFLAGS}.*\"/:/" -i configure.ac
%endif

export OPT="%{optflags} -g"

# to fix curses module build
# https://bugs.mageia.org/show_bug.cgi?id=6702
export CFLAGS="%{optflags} -D_GNU_SOURCE -fPIC -fwrapv -I/usr/include/ncursesw"
export CPPFLAGS="%{optflags} -D_GNU_SOURCE -fPIC -fwrapv -I/usr/include/ncursesw"

# Python's configure adds -std=c99 even for c++, clang doesn't like that
# combination at all
sed -i -e 's,-std=c99,,' configure.ac

autoreconf -vfi
%configure	--with-threads \
		--enable-ipv6 \
		--with-wide-unicode \
		--with-dbmliborder=gdbm \
%if %{with pip}
		--with-ensurepip=install \
%else
		--without-ensurepip \
%endif
		--with-system-expat \
		--with-cxx-main=%{__cxx} \
		--with-system-ffi \
		--enable-loadable-sqlite-extensions \
		--enable-shared \
		--enable-optimizations \
		--with-pymalloc \
		--enable-ipv6=yes \
		--with-system-expat \
		--with-computed-gotos \
%if %{with valgrind}
		--with-valgrind
%endif

# fix build
#perl -pi -e 's/^(LDFLAGS=.*)/$1 -lstdc++/' Makefile
# (misc) if the home is nfs mounted, rmdir fails due to delay
export TMP="/tmp" TMPDIR="/tmp"
# This is used for bootstrapping - and we don't want to
# require ourselves
sed -i -e 's,env python,python2,' Python/makeopcodetargets.py
%make PYTHON=python2 -j1

%check
# (misc) if the home is nfs mounted, rmdir fails
export TMP="/tmp" TMPDIR="/tmp"

# Currently (3.3.0-1), LOTS of tests fail, but python3 seems to work
# quite fine anyway. Chances are something in the testsuite itself is bogus.
#make test TESTOPTS="-w -x test_linuxaudiodev -x test_nis -x test_shutil -x test_pyexpat -x test_minidom -x test_sax -x test_string -x test_str -x test_unicode -x test_userstring -x test_bytes -x test_distutils -x test_mailbox -x test_ioctl -x test_telnetlib -x test_strtod -x test_urllib2net -x test_runpy -x test_posix -x test_robotparser -x test_numeric_tower -x test_math -x test_cmath -x test_importlib -x test_import -x test_float -x test_strtod -x test_timeout"

%install
mkdir -p %{buildroot}%{_prefix}/lib/python%{dirver}

# fix Makefile to get rid of reference to distcc
perl -pi -e "/^CC=/ and s/distcc/gcc/" Makefile

# set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"%{buildroot}%{_bindir}" >>setup.cfg

# python is not GNU and does not know fsstd
mkdir -p %{buildroot}%{_mandir}
%makeinstall_std LN="ln -sf"

(cd %{buildroot}%{_libdir}; ln -sf `ls libpython%{api}*.so.*` libpython%{api}.so)

# Work around broken distutils having no idea about the need to link
# python modules to libpython (it probably should get this information
# from _sysconfigdata.py rather than parsing a Makefile?)
%if %{with abi_m}
cat >>%{buildroot}%{_libdir}/python%{dirver}/config-%{dirver}m/Makefile <<EOF
%else
cat >>%{buildroot}%{_libdir}/python%{dirver}/config-%{dirver}/Makefile <<EOF
%endif

Py_ENABLE_SHARED= 1
EOF

# install pynche
cat << EOF > %{buildroot}%{_bindir}/pynche
#!/bin/bash
exec %{_libdir}/python%{dirver}/site-packages/pynche/pynche
EOF
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche %{buildroot}%{_libdir}/python%{dirver}/site-packages/

chmod 755 %{buildroot}%{_bindir}/{idle3,pynche}

ln -f Tools/pynche/README Tools/pynche/README.pynche

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-tkinter3.6.desktop << EOF
[Desktop Entry]
Name=IDLE
Comment=IDE for Python3.6
Exec=%{_bindir}/idle3.6
Icon=development_environment_section
Terminal=false
Type=Application
Categories=Development;IDE;
EOF


cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-docs.desktop << EOF
[Desktop Entry]
Name=Python documentation
Comment=Python complete reference
Exec=%{_bindir}/xdg-open %{_defaultdocdir}/%{name}-docs/index.html
Icon=documentation_section
Terminal=false
Type=Application
Categories=Documentation;
EOF


# fix non real scripts
#chmod 644 %{buildroot}%{_libdir}/python*/test/test_{binascii,grp,htmlparser}.py*
find %{buildroot} -type f \( -name "test_binascii.py*" -o -name "test_grp.py*" -o -name "test_htmlparser.py*" \) -exec chmod 644 {} \;
# fix python library not stripped
chmod u+w %{buildroot}%{_libdir}/libpython%{api}*.so.1.0 %{buildroot}%{_libdir}/libpython3.so

# drop backup files
find %{buildroot} -name "*~" -exec rm -f {} \;

mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -m644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/rpm/macros.d/

# Fix permissions on docs
find html -type d |xargs chmod 0755
find html -type f |xargs chmod 0644

# remove  stuff provided by system python 3
rm -f %{buildroot}%{_bindir}/{2to3,pydoc3,python3,pyvenv,pip3,python3-config}
rm -f %{buildroot}%{_libdir}/pkgconfig/python3.pc
rm -f %{buildroot}%{_mandir}/man1/python3.1*
rm -f %{buildroot}%{_libdir}/libpython3.so

%files
%doc README.omv
%{_sysconfdir}/rpm/macros.d/*.macros
%{_includedir}/python*/pyconfig.h

%dir %{_libdir}/python*/config-*
%{_libdir}/python*/config*/Makefile
%exclude %{_libdir}/python*/site-packages/pynche
%exclude %{_libdir}/python*/lib-dynload/_tkinter.*.so

# HACK: build fails without this (TODO: investigate rpm)
%dir %{_libdir}/python*
%{_libdir}/python*/LICENSE.txt
%{_libdir}/python%{dirver}/*.py
%{_libdir}/python%{dirver}/__pycache__
%{_libdir}/python%{dirver}/asyncio
%{_libdir}/python%{dirver}/collections
%{_libdir}/python%{dirver}/concurrent
%{_libdir}/python%{dirver}/ctypes
%{_libdir}/python%{dirver}/curses
%{_libdir}/python%{dirver}/dbm
%{_libdir}/python%{dirver}/distutils
%{_libdir}/python%{dirver}/email
%{_libdir}/python%{dirver}/encodings
%{_libdir}/python%{dirver}/ensurepip
%{_libdir}/python%{dirver}/html
%{_libdir}/python%{dirver}/http
%{_libdir}/python%{dirver}/importlib
%{_libdir}/python%{dirver}/json
%{_libdir}/python%{dirver}/lib-dynload
%{_libdir}/python%{dirver}/lib2to3
%{_libdir}/python%{dirver}/logging
%{_libdir}/python%{dirver}/multiprocessing
%{_libdir}/python%{dirver}/pydoc_data
%{_libdir}/python%{dirver}/site-packages
%{_libdir}/python%{dirver}/sqlite3
%{_libdir}/python%{dirver}/turtledemo
%{_libdir}/python%{dirver}/unittest
%{_libdir}/python%{dirver}/urllib
%{_libdir}/python%{dirver}/venv
%{_libdir}/python%{dirver}/wsgiref*
%{_libdir}/python%{dirver}/xml
%{_libdir}/python%{dirver}/xmlrpc
%{_bindir}/pydoc%{dirver}
%{_bindir}/python%{dirver}*
%{_bindir}/pyvenv-%{dirver}
%{_bindir}/2to3-%{dirver}
%exclude %{_bindir}/python*config
%{_mandir}/man*/*
# pip bits
%if %{with pip}
%if "%{_libdir}" != "%{_prefix}/lib"
# In the %{_libdir} == %{_prefix}/lib case, those are caught by
# globs above.
%dir %{_prefix}/lib/python%{dirver}
%dir %{_prefix}/lib/python%{dirver}/site-packages
%{_prefix}/lib/python%{dirver}/site-packages/__pycache__
%{_prefix}/lib/python%{dirver}/site-packages/pkg_resources.py
%{_prefix}/lib/python%{dirver}/site-packages/easy_install.py
%{_prefix}/lib/python%{dirver}/site-packages/pip
%{_prefix}/lib/python%{dirver}/site-packages/setuptools*
%{_prefix}/lib/python%{dirver}/site-packages/_markerlib
%{_prefix}/lib/python%{dirver}/site-packages/pip-*.dist-info
%endif
%{_bindir}/easy_install-%{dirver}
%{_bindir}/pip%{dirver}
%endif

%files -n %{libname}
%if %{with abi_m}
%{_libdir}/libpython%{api}m.so.%{major}*
%else
%{_libdir}/libpython%{api}.so.%{major}*
%endif

%files -n %{devname}
%{_libdir}/libpython*.so
%{_includedir}/python*
%{_libdir}/python*/config-%{dirver}*
%{_libdir}/python*/test/
%{_bindir}/python%{dirver}*-config
%{_libdir}/pkgconfig/python*.pc
%exclude %{_includedir}/python*/pyconfig.h
%exclude %{_libdir}/python*/config*/Makefile

%files docs
%doc html/*/*
%{_datadir}/applications/mandriva-%{name}-docs.desktop

%files -n tkinter3.6
%{_libdir}/python*/tkinter/
%{_libdir}/python*/idlelib
%{_libdir}/python*/site-packages/pynche
%{_libdir}/python*/lib-dynload/_tkinter.*.so

%files -n tkinter3.6-apps
%{_bindir}/idle3*
%{_bindir}/pynche
%{_datadir}/applications/mandriva-tkinter3.6.desktop
