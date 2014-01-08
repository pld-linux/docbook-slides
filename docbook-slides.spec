Summary:	DocBook Slides document type and stylesheets
Name:		docbook-slides
Version:	3.4.0
Release:	1
License:	MIT
Group:		Applications/Publishing/XML
Source0:	http://downloads.sourceforge.net/docbook/%{name}-%{version}.tar.gz
# Source0-md5:	26e2083077454d7140f2b82ae3d66123
Source1:	%{name}.xml
Source2:	%{name}.cat
URL:		http://sourceforge.net/projects/docbook
Requires(post,preun):	/usr/bin/install-catalog
Requires(post,preun):	/usr/bin/xmlcatalog
Requires:	libxml2-progs >= 2.4.17-6
Requires:	sgml-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dtd_path	%{_datadir}/sgml/docbook/slides/%{version}
%define		xmlcat_file	%{dtd_path}/catalog.xml
%define		sgmlcat_file	%{dtd_path}/catalog

%description
DocBook Slides provides customization layers of the both the
Simplified and the full DocBook XML DTD, as well as the DocBook XSL
Stylesheets. This package contains the XML document type definition
and stylesheets for processing DocBook Slides XML. The slides doctype
and stylesheets are for generating presentations, primarily in HTML.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{dtd_path}

cp -a browser graphics schema xsl VERSION $RPM_BUILD_ROOT%{dtd_path}

install %{SOURCE1} $RPM_BUILD_ROOT%{xmlcat_file}
install %{SOURCE2} $RPM_BUILD_ROOT%{sgmlcat_file}

%docbook_sgmlcat_fix $RPM_BUILD_ROOT%{sgmlcat_file} %{version}

%xmlcat_add_rewrite \
	http://www.oasis-open.org/docbook/xml/%{version} \
	file://%{dtd_path} \
	$RPM_BUILD_ROOT%{xmlcat_file}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q /etc/sgml/slides.cat /etc/sgml/catalog ; then
	%sgmlcat_add /etc/sgml/slides.cat %{sgmlcat_file}

fi
if ! grep -q %{xmlcat_file} /etc/xml/catalog ; then
	%xmlcat_add %{xmlcat_file}

fi

%preun
if [ "$1" = "0" ] ; then
	%sgmlcat_del /etc/sgml/slides.cat %{sgmlcat_file}
	%xmlcat_del %{xmlcat_file}
fi

%files
%defattr(644,root,root,755)
%doc BUGS NEWS README RELEASE-NOTES.txt TODO doc
%dir %{_datadir}/sgml/docbook/slides
%{dtd_path}
