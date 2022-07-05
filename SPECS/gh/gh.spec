Summary:        GitHub official command line tool
Name:           gh
Version:        2.13.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/cli/cli
Source0:        https://github.com/cli/cli/archive/refs/tags/v%{version}.tar.gz#/cli-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/cli/cli/archive/refs/tags/v%{version}.tar.gz -O cli-%%{version}.tar.gz
#   2. tar -xf cli-%%{version}.tar.gz
#   3. cd cli-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor.tar.gz

BuildRequires:  golang >= 1.17.1
BuildRequires:  git
BuildRequires:  bash-completion
BuildRequires:  fish
BuildRequires:  zsh
Requires:       bash-completion
Requires:       fish
Requires:       zsh
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
GitHub official command line tool.

%prep
%setup -q -n cli-%{version}

%build
tar --no-same-owner -xf %{SOURCE1}
export GOPATH=%{our_gopath}
# No mod download use vednor cache locally
export GOFLAGS="-buildmode=pie -trimpath -mod=vendor -modcacherw -ldflags=-linkmode=external"
make GH_VERSION="v%{version}" bin/gh manpages

%install
./bin/gh completion -s bash | install -Dm644 /dev/stdin %{buildroot}%{_datadir}/bash-completion/completions/gh
./bin/gh completion -s fish | install -Dm644 /dev/stdin %{buildroot}%{_datadir}/fish/vendor_completions.d/gh.fish
./bin/gh completion -s zsh | install -Dm644 /dev/stdin %{buildroot}%{_datadir}/zsh/site-functions/_gh

install -Dm755 bin/gh %{buildroot}%{_bindir}/gh
install -d %{buildroot}%{_mandir}/man1/
cp share/man/man1/* %{buildroot}%{_mandir}/man1

%check
make test

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/gh
%{_mandir}/man1/*
%{_datadir}/bash-completion/completions/gh
%{_datadir}/fish/vendor_completions.d/gh.fish
%{_datadir}/zsh/site-functions/_gh

%changelog
* Thu Jun 30 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.13.0-1
- Original version for CBL-Mariner.
- License verified.
