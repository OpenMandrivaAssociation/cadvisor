%global provider        github
%global provider_tld    com
%global project         google
%global repo            cadvisor
# https://github.com/google/cadvisor
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          546a3771589bdb356777c646c6eca24914fdd48b
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           %{repo}
Version:        0.33.1
Release:        3
Summary:        Analyzes resource usage and performance characteristics of running containers
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{version}.tar.gz
Source1:        cadvisor
Source2:        cadvisor.service

# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}

cAdvisor (Container Advisor) provides container users an understanding of the
resource usage and performance characteristics of their running containers.
It is a running daemon that collects, aggregates, processes, and exports
information about running containers. Specifically, for each container it keeps
resource isolation parameters, historical resource usage, histograms of
complete historical resource usage and network statistics. This data is
exported by container and machine-wide.

cAdvisor currently supports lmctfy containers as well as Docker containers
(those that use the default libcontainer execdriver). Other container backends
can also be added. cAdvisor's container abstraction is based on lmctfy's
so containers are inherently nested hierarchically.


%prep
%autosetup
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%build
export GOPATH=%{_builddir}:$(pwd):%{gopath}
%gobuild -o bin/cadvisor %{import_path}

%install
# main package binary
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/cadvisor %{buildroot}%{_bindir}

# install systemd/sysconfig 
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 0660 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -d -m 0755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service

%post
%systemd_post cadvisor.service

%preun
%systemd_preun cadvisor.service

%postun
%systemd_postun cadvisor.service

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc CHANGELOG.md README.md CONTRIBUTING.md AUTHORS
%doc Godeps/Godeps.json
%{_bindir}/cadvisor
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
