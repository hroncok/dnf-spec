%global hawkey_version 0.7.1
%global librepo_version 1.7.19
%global libcomps_version 0.1.8
%global rpm_version 4.13.0-0.rc1.29
%global min_plugins_core 0.1.13
%global dnf_langpacks_ver 0.15.1-6

%global confdir %{_sysconfdir}/%{name}

%global pluginconfpath %{confdir}/plugins
%global py2pluginpath %{python2_sitelib}/%{name}-plugins

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

%if %{with python3}
%global py3pluginpath %{python3_sitelib}/%{name}-plugins
%endif

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

Name:           dnf
Version:        2.0.1
Release:        2%{?dist}
Summary:        Package manager forked from Yum, using libsolv as a dependency resolver
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:        GPLv2+ and GPLv2 and GPL
URL:            https://github.com/rpm-software-management/dnf
Source0:        %{url}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
# https://bugzilla.redhat.com/show_bug.cgi?id=1380945
Patch666:       0001-Revert-group-treat-mandatory-pkgs-as-mandatory-if-st.patch
BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  python-bugzilla
BuildRequires:  python-sphinx
BuildRequires:  systemd
BuildRequires:  bash-completion
%if %{with python3}
Requires:       python3-%{name} = %{version}-%{release}
%else
Requires:       python2-%{name} = %{version}-%{release}
%endif
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
Provides:       dnf-command(autoremove)
Provides:       dnf-command(check-update)
Provides:       dnf-command(clean)
Provides:       dnf-command(distro-sync)
Provides:       dnf-command(downgrade)
Provides:       dnf-command(group)
Provides:       dnf-command(history)
Provides:       dnf-command(info)
Provides:       dnf-command(install)
Provides:       dnf-command(list)
Provides:       dnf-command(makecache)
Provides:       dnf-command(mark)
Provides:       dnf-command(provides)
Provides:       dnf-command(reinstall)
Provides:       dnf-command(remove)
Provides:       dnf-command(repolist)
Provides:       dnf-command(repoquery)
Provides:       dnf-command(repository-packages)
Provides:       dnf-command(search)
Provides:       dnf-command(updateinfo)
Provides:       dnf-command(upgrade)
Provides:       dnf-command(upgrade-to)
Conflicts:      python2-dnf-plugins-core < %{min_plugins_core}
Conflicts:      python3-dnf-plugins-core < %{min_plugins_core}

# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      dnf-langpacks < %{dnf_langpacks_ver}

%description
Package manager forked from Yum, using libsolv as a dependency resolver.

%package conf
Summary:        Configuration files for DNF
Requires:       libreport-filesystem
# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      dnf-langpacks-conf < %{dnf_langpacks_ver}

%description conf
Configuration files for DNF.

%package yum
Conflicts:      yum < 3.4.3-505
Requires:       %{name} = %{version}-%{release}
Summary:        As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF

%description yum
As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF.

%package -n python2-%{name}
Summary:        Python 2 interface to DNF
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:  python2-devel
BuildRequires:  python-hawkey >= %{hawkey_version}
BuildRequires:  python-iniparse
BuildRequires:  python-libcomps >= %{libcomps_version}
BuildRequires:  python-librepo >= %{librepo_version}
BuildRequires:  python-nose
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  pygpgme
%else
BuildRequires:  python2-pygpgme
%endif
BuildRequires:  pyliblzma
BuildRequires:  rpm-python >= %{rpm_version}
Requires:       pyliblzma
Requires:       %{name}-conf = %{version}-%{release}
Requires:       deltarpm
Requires:       python-hawkey >= %{hawkey_version}
Requires:       python-iniparse
Requires:       python-libcomps >= %{libcomps_version}
Requires:       python-librepo >= %{librepo_version}
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       pygpgme
%else
Requires:       python2-pygpgme
%endif
Requires:       rpm-plugin-systemd-inhibit
Requires:       rpm-python >= %{rpm_version}
# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      python-dnf-langpacks < %{dnf_langpacks_ver}

%description -n python2-%{name}
Python 2 interface to DNF.

%if %{with python3}
%package -n python3-%{name}
Summary:        Python 3 interface to DNF.
%{?system_python_abi}
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
BuildRequires:  python3-hawkey >= %{hawkey_version}
BuildRequires:  python3-iniparse
BuildRequires:  python3-libcomps >= %{libcomps_version}
BuildRequires:  python3-librepo >= %{librepo_version}
BuildRequires:  python3-nose
BuildRequires:  python3-pygpgme
BuildRequires:  rpm-python3 >= %{rpm_version}
Requires:       %{name}-conf = %{version}-%{release}
Requires:       deltarpm
Requires:       python3-hawkey >= %{hawkey_version}
Requires:       python3-iniparse
Requires:       python3-libcomps >= %{libcomps_version}
Requires:       python3-librepo >= %{librepo_version}
Requires:       python3-pygpgme
Requires:       rpm-plugin-systemd-inhibit
Requires:       rpm-python3 >= %{rpm_version}
# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      python3-dnf-langpacks < %{dnf_langpacks_ver}

%description -n python3-%{name}
Python 3 interface to DNF.
%endif

%package automatic
Summary:        Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.
BuildRequires:  systemd
Requires:       %{name} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description automatic
Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.

%prep
%autosetup -p1
mkdir build
%if %{with python3}
mkdir build-py3
%endif

%build
pushd build
  %cmake ..
  %make_build
  make doc-man
popd
%if %{with python3}
pushd build-py3
  %cmake .. -DPYTHON_DESIRED:str=3 -DWITH_MAN=0
  %make_build
popd
%endif

%install
pushd build
  %make_install
popd
%if %{with python3}
pushd build-py3
  %make_install
popd
%endif
%find_lang %{name}

mkdir -p %{buildroot}%{pluginconfpath}/
mkdir -p %{buildroot}%{py2pluginpath}/
%if %{with python3}
mkdir -p %{buildroot}%{py3pluginpath}/__pycache__/
%endif
mkdir -p %{buildroot}%{_localstatedir}/log/
mkdir -p %{buildroot}%{_var}/cache/dnf/
touch %{buildroot}%{_localstatedir}/log/%{name}.log
%if %{with python3}
%{?system_python_abi:sed -i 's|#!%{__python3}|#!%{_libexecdir}/system-python|' %{buildroot}%{_bindir}/{dnf-3,yum}}
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
%else
ln -sr %{buildroot}%{_bindir}/dnf-2 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-2 %{buildroot}%{_bindir}/dnf-automatic
%endif
rm -vf %{buildroot}%{_bindir}/dnf-automatic-*

%check
pushd build
  ctest -VV
popd
%if %{with python3}
pushd build-py3
  ctest -VV
popd
%endif

%post
%systemd_post dnf-makecache.timer

%preun
%systemd_preun dnf-makecache.timer

%postun
%systemd_postun_with_restart dnf-makecache.timer

%post automatic
%systemd_post dnf-automatic-notifyonly.timer
%systemd_post dnf-automatic-download.timer
%systemd_post dnf-automatic-install.timer

%preun automatic
%systemd_preun dnf-automatic-notifyonly.timer
%systemd_preun dnf-automatic-download.timer
%systemd_preun dnf-automatic-install.timer

%postun automatic
%systemd_postun_with_restart dnf-automatic-notifyonly.timer
%systemd_postun_with_restart dnf-automatic-download.timer
%systemd_postun_with_restart dnf-automatic-install.timer

%files -f %{name}.lang
%{_bindir}/%{name}
%if 0%{?rhel} && 0%{?rhel} <= 7
%{_sysconfdir}/bash_completion.d/%{name}
%else
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%endif
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/yum2dnf.8*
%{_unitdir}/%{name}-makecache.service
%{_unitdir}/%{name}-makecache.timer
%{_var}/cache/%{name}/

%files conf
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%dir %{confdir}
%dir %{pluginconfpath}
%dir %{confdir}/protected.d
%config(noreplace) %{confdir}/%{name}.conf
%config(noreplace) %{confdir}/protected.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%ghost %{_localstatedir}/log/hawkey.log
%ghost %{_localstatedir}/log/%{name}.log
%ghost %{_localstatedir}/log/%{name}.librepo.log
%ghost %{_localstatedir}/log/%{name}.rpm.log
%ghost %{_localstatedir}/log/%{name}.plugin.log
%ghost %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/groups.json
%ghost %{_sharedstatedir}/%{name}/yumdb
%ghost %{_sharedstatedir}/%{name}/history
%{_mandir}/man5/%{name}.conf.5.gz
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf

%files yum
%{_bindir}/yum
%{_mandir}/man8/yum.8.gz

%files -n python2-%{name}
%{_bindir}/%{name}-2
%exclude %{python2_sitelib}/%{name}/automatic
%{python2_sitelib}/%{name}/
%dir %{py2pluginpath}

%if %{with python3}
%files -n python3-%{name}
%{_bindir}/%{name}-3
%exclude %{python3_sitelib}/%{name}/automatic
%{python3_sitelib}/%{name}/
%dir %{py3pluginpath}
%dir %{py3pluginpath}/__pycache__
%endif

%files automatic
%{_bindir}/%{name}-automatic
%config(noreplace) %{confdir}/automatic.conf
%{_mandir}/man8/%{name}.automatic.8.gz
%{_unitdir}/%{name}-automatic-notifyonly.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-download.service
%{_unitdir}/%{name}-automatic-download.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-install.timer
%if %{with python3}
%{python3_sitelib}/%{name}/automatic/
%else
%{python2_sitelib}/%{name}/automatic/
%endif

%changelog
* Thu Feb 09 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.1-2
- Update to 2.0.1

* Thu Dec 15 2016 mluscon <mluscon@redhat.com> - 2.0.0-2
- rebuild py36

* Wed Dec 14 2016 Michal Luscon <mluscon@redhat.com> 2.0.0-1
- tests: catch ModuleNotFoundError as well (Igor Gnatenko)
- Switch out automatic service for automatic-download and automatic-install
  (Pat Riehecky)
- Make upgrade-to alias for upgrade (RhBug:1327999) (Jaroslav Mracek)
- skip appending an empty option (RhBug: 1400081) (Michael Mraka)
- Add description of nevra foems for commands and autoremove args (Jaroslav
  Mracek)
- Add support of arguments nevra forms for autoremove command (Jaroslav Mracek)
- Add nevra forms for remove command (Jaroslav Mracek)
- Add nevra forms for install command (Jaroslav Mracek)
- add bin/yum into .gitignore (Michal Luscon)
- clean: acquire all locks before cleaning (RhBug:1293782) (Michal Luscon)
- Change hawkey version requirement (Jaroslav Mracek)
- Add information for translators (RhBug:1386078) (Jaroslav Mracek)
- Change info to warning for clean repoquery output (RhBug:1358245) (Jaroslav
  Mracek)
- Add description of pkg flag for Query (RhBug:1243393) (Jaroslav Mracek)
- Add minor changes in documentation (Jaroslav Mracek)
- Do not always overwrite the name with the repo ID (Neal Gompa)

* Tue Dec 06 2016 Martin Hatina <mhatina@redhat.com> - 2.0.0-0.rc2.5
- Fix libdnf requirement version

* Tue Dec 06 2016 Martin Hatina <mhatina@redhat.com> - 2.0.0-0.rc2.4
- Increase requirement of libdnf

* Sun Dec 04 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-0.rc2.3
- Restore patch for relaxing strict groups

* Fri Dec 02 2016 Martin Hatina <mhatina@redhat.com> 2.0.0-0.rc2.2
- Restore changelog

* Fri Dec 02 2016 Martin Hatina <mhatina@redhat.com> 2.0.0-0.rc2.1
- See http://dnf.readthedocs.io/en/latest/release_notes.html

* Thu Oct 06 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-0.rc1.4
- Fix crash in repoquery
- Trim changelog

* Tue Oct 04 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-0.rc1.3
- Revert group install strict bugfix (RHBZ #1380945)

* Fri Sep 30 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.0.0-0.rc1.2
- Add alias 'rpm' for 'type=' option (RHBZ #1380580)

* Thu Sep 29 2016 Michal Luscon <mluscon@redhat.com> 2.0.0-0.rc1.1
- See http://dnf.readthedocs.io/en/latest/release_notes.html

* Thu Sep 08 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.10-2
- Obsolete dnf-langpacks
- Backport patch for dnf repolist disabled

* Thu Aug 18 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.10-1
- Update to 1.1.10

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.9-6
- Fix typo

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.9-5
- Also change shebang for %%{?system_python_abi} in %%{_bindir}/dnf

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.9-4
- Add %%{?system_python_abi}

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 24 2016 Michal Luscon <mluscon@redhat.com> 1.1.9-2
- Revert "group: treat mandatory pkgs as mandatory if strict=true" (RhBug:1337731)
- enforce-api: reflect changes from #992475 in completion_helper (RhBug:1338504)
- enforce-api: add compatibility methods for renamed counterparts (RhBug:1338564)

* Thu May 19 2016 Igor Gnatenko <ignatenko@redhat.com> 1.1.9-1
- doc: release notes 1.1.9 (Igor Gnatenko)
- spec: correctly set up requirements for python subpkg (Igor Gnatenko)
- spec: follow new packaging guidelines & make compatible with el7 (Igor
  Gnatenko)
- zanata update (Jan Silhan)
- enforce-api: add missing bits of Base class (Michal Luscon)
- help: unify help msg strings (Michal Luscon)
- enforce-api: decorate Base class (Michal Luscon)
- util: add decorator informing users of nonapi functions (Michal Luscon)
- Added description for 'autoremove' in dnf help (RhBug:1324086) (Abhijeet
  Kasurde)
- i18n: fixup for 0db13feed (Michal Luscon)
- i18n: use fallback mode if terminal does not support UTF-8 (RhBug:1332012)
  (Michal Luscon)
- Revert "spec: follow new packaging guidelines & make compatible with el7"
  (Michal Luscon)
- move autoglob feature directly to filterm() and filter() (Michael Mraka)
- group: treat mandatory pkgs as mandatory if strict=true (RhBug:1292892)
  (Michal Luscon)
- locks: fix lock paths in tmpfsd config since cachedir has been changed
  (Michal Luscon)
- remove formating from translation strings (Michal Luscon)
- base: set diskspace check filter before applying the filters (RhBug:1328674)
  (Michal Luscon)
- order repos by priority and cost (Michael Mraka)
- spec: follow new packaging guidelines & make compatible with el7 (Igor
  Gnatenko)
- bash-completion: first try to set fallback to BASH_COMPLETION_COMPATDIR (Igor
  Gnatenko)
- updated copyrights for files changed this year (Michael Mraka)
- cli: fix warning from re.split() about non-empty pattern (RhBug:1286556)
  (Igor Gnatenko)
- update authors file (Michal Luscon)
- Define __hash__ method for YumHistoryPackage (RhBug:1245121) (Max Prokhorov)

* Tue Apr 05 2016 Michal Luscon <mluscon@redhat.com> 1.1.8-1
- refactor: repo: add md_expired property (Michal Domonkos)
- test: fix cachedir usage in LocalRepoTest (Michal Domonkos)
- clean: operate on all cached repos (RhBug:1278225) (Michal Domonkos)
- refactor: repo: globally define valid repoid chars (Michal Domonkos)
- RepoPersistor: only write to disk when requested (Michal Domonkos)
- clean: remove dead subcommands (Michal Domonkos)
- doc: --best in case of problem (RhBug:1309408) (Jan Silhan)
- Added fix for correct error message for group info (RhBug:1209649) (Abhijeet
  Kasurde)
- repo: don't get current timeout for librepo (RhBug:1272977) (Igor Gnatenko)
- doc: fix default timeout value (Michal Luscon)
- cli: inform only about nonzero md cache check interval (Michal Luscon)
- base: report errors in batch at the end of md downloading (Michal Luscon)
- repo: produce more sane error if md download fails (Michal Luscon)
- zanata update (RhBug:1322226) (Jan Silhan)
- doc: Fixed syntax of `assumeyes` and `defaultyes` ref lables in
  `conf_ref.rst` (Matt Sturgeon)
- Fix output headers for dnf history command (Michael Dunphy)
- doc: change example of 'dnf-command(repoquery)' (Jaroslav Mracek)
- makacache.service: shorten journal logs (RhBug:1315349) (Michal Luscon)
- config: improve UX of error msg (Michal Luscon)
- Added user friendly message for out of range value (RhBug:1214562) (Abhijeet
  Kasurde)
- doc: prefer repoquery to list (Jan Silhan)
- history: fix empty history cmd (RhBug:1313215) (Michal Luscon)
- Very minor tweak to the docs for `--assumeyes` and `--assumeno` (Matt
  Sturgeon)

* Thu Feb 25 2016 Michal Luscon <mluscon@redhat.com> 1.1.7-1
- Add `/etc/distro.repos.d` as a path owned by the dnf package (Neal Gompa
  (ニール・ゴンパ))
- Change order of search and add new default repodirs (RhBug:1286477) (Neal
  Gompa (ニール・ゴンパ))
- group: don't mark available packages as installed (RhBug:1305356) (Jan
  Silhan)
- history: adjust demands for particular subcommands (RhBug:1258503) (Michal
  Luscon)
- Added extension command for group list (RhBug:1283432) (Abhijeet Kasurde)
- perf: dnf repository-packages <repo> upgrade (RhBug:1306304) (Jan Silhan)
- sack: Pass base.conf.substitutions["arch"] to sack in build_sack() function.
  (Daniel Mach)
- build: make python2/3 binaries at build time (Michal Domonkos)
- fix dnf history traceback (RhBug:1303149) (Jan Silhan)
- cli: truncate expiration msg (RhBug:1302217) (Michal Luscon)

* Mon Jan 25 2016 Michal Luscon <mluscon@redhat.com> 1.1.6-1
- history: don't fail if there is no history (RhBug:1291895) (Michal Luscon)
- Allow dnf to use a socks5 proxy, since curl support it (RhBug:1256587)
  (Michael Scherer)
- output: do not log rpm info twice (RhBug:1287221) (Michal Luscon)
- dnf owns /var/lib/dnf dir (RhBug:1294241) (Jan Silhan)
- Fix handling of repo that never expire (RhBug:1289166) (Jaroslav Mracek)
- Filter out .src packages when multilib_proto=all (Jeff Smith)
- Enable string for translation (RhBug:1294355) (Parag Nemade)
- Let logging format messages on demand (Ville Skyttä)
- clean: include metadata of local repos (RhBug:1226322) (Michal Domonkos)
- completion: Install to where bash-completion.pc says (Ville Skyttä)
- spec: bash completion is not a %%config file (Ville Skyttä)
- Change assertion handling for rpmsack.py (RhBug:1275878) (Jaroslav Mracek)
- cli: fix storing arguments in history (RhBug:1239274) (Ting-Wei Lan)

* Thu Dec 17 2015 Michal Luscon <mluscon@redhat.com> 1.1.5-1
- base: save group persistor only after successful transaction (RhBug:1229046)
  (Michal Luscon)
- base: do not clean tempfiles after remove transaction (RhBug:1282250) (Michal
  Luscon)
- base: clean packages that do not belong to any trans (Michal Luscon)
- upgrade: allow group upgrade via @ syntax (RhBug:1265391) (Michal Luscon)
- spec: Mark license files as %%license where available (Ville Skyttä)
- Remove unused imports (Ville Skyttä)
- Spelling fixes (Ville Skyttä)
- Fix typos in documentation (Rob Cutmore)
- parser: add support for braces in substitution (RhBug:1283017) (Dave
  Johansen)
- completion_helper: Don't omit "packages" from clean completions (Ville
  Skyttä)
- bash-completion: Avoid unnecessary python invocation per _dnf_helper (Ville
  Skyttä)
- repo: Download drpms early (RhBug:1260421) (Ville Skyttä)
- clean: Don't hardcode list of args in two places (Ville Skyttä)
- cli: don't crash if y/n and sys.stdin is None (RhBug:1278382) (Adam
  Williamson)
- sp err "environement" -> "environment" (Michael Goodwin)
- Remove -OO from #!/usr/bin/python (RhBug:1230820) (Jaroslav Mracek)
- cli: warn if plugins are disabled (RhBug:1280240) (Michal Luscon)

* Mon Nov 16 2015 Michal Luscon <mluscon@redhat.com> 1.1.4-1
- AUTHORS: updated (Jan Silhan)
- query: add compatibility methods (Michal Luscon)
- query: add recent, extras and autoremove methods to Query (Michal Luscon)
- query: add duplicated and latest-limit queries into api (Michal Luscon)
- format the email message with its as_string method (Olivier Andrieu)
- added dnf.i18n.ucd* functions as deprecated API (Jan Silhan)
- i18n: unicode resulting translations (RhBug:1278031) (Jan Silhan)
- po: get rid of new lines in translation (Jan Silhan)
- output: add skip count to summary (RhBug:1264032) (Michal Domonkos)
- groups: fix environment upgrade (Michal Luscon)
- Fix plural strings extraction (RhBug:1209056) (Baurzhan Muftakhidinov)
- po: fixed malformed beginning / ending (Jan Silhan)
- zanata update (Jan Silhan)
- cli: prevent tracebacks after C^ (RhBug:1274946) (Michal Luscon)

* Wed Oct 14 2015 Michal Luscon <mluscon@redhat.com> 1.1.3-1
- Update command_ref.rst (Jaroslav Mracek)
- Change in automatic.conf email settings to prevent email error with default
  sender name (Jaroslav Mracek)
- Replace assert_called() with assert_called_with() for Py35 support (Neal
  Gompa (ニール・ゴンパ))
- doc: improve documentation (Jaroslav Mracek)
- doc: update the instructions related to nightly builds (Radek Holy)
- Revert "Add the continuous integration script" (Radek Holy)
- Revert "cosmetic: ci: fix the Copr name in the README" (Radek Holy)
- Fix typo in Command.canonical's doctring (Timo Wilken)
- base: group_install is able to exclude mandatory packages
  (Related:RhBug:1199868) (Jan Silhan)

* Wed Sep 30 2015 Michal Luscon <mluscon@redhat.com> 1.1.2-4
- don't import readline as it causes crashes in Anaconda
  (related:RhBug:1258364)

* Tue Sep 22 2015 Michal Luscon <mluscon@redhat.com> 1.1.2-3
- Revert "completion_helper: don't get IndexError (RhBug:1250038)"

* Tue Sep 22 2015 Michal Luscon <mluscon@redhat.com> 1.1.2-2
- add hawkey version requirement
- revert commit #70956

* Tue Sep 22 2015 Michal Luscon <mluscon@redhat.com> 1.1.2-1
- doc: release notes 1.1.2 (Michal Luscon)
- sanitize non Unicode command attributes (RhBug:1262082) (Jan Silhan)
- don't redirect confirmation to stderr RhBug(1258364) (Vladan Kudlac)
- clean: add rpmdb to usage (Vladan Kudlac)
- completion_helper: don't get IndexError (RhBug:1250038) (Vladan Kudlac)
- add --downloadonly switch (RhBug:1048433) (Adam Salih)
- Add globbing support to base.by_provides() (RhBug:11259650) (Valentina
  Mukhamedzhanova)
- spec: packaging python(3)-dnf according to new Fedora guidelines
  (RhBug:1260198) (Jaroslav Mracek)
- Bug in Source0: URL in dnf.spec fixed (RhBug:126255) (Jaroslav Mracek)
- To dnf.spec added provides dnf-command(command name) for 21 dnf commands
  (RhBug:1259657) (jmracek)
- Expire repo cache on failed package download (Valentina Mukhamedzhanova)
- cosmetic: ci: fix the Copr name in the README (Radek Holy)
- Add the continuous integration script (Radek Holy)
- Set proper charset on email in dnf-automatic (RhBug:1254982) (Valentina
  Mukhamedzhanova)
- doc: improve configuration description (RhBug:1261766) (Michal Luscon)
- remove: show from which repo a package is (Vladan Kudlac)
- list: show from which repo a package is (RhBug:1234491) (Vladan Kudlac)
- Spelling/grammar fixes (Ville Skyttä)
- install: fix crash when terminal window is small (RhBug:1256531) (Vladan
  Kudlac)
- install: mark unification of the progress bar (Vladan Kudlac)
- fix translations in python3 (RhBug:1254687) (Michal Luscon)
- group: CompsQuery now returns group ids (RhBug:1261656) (Michal Luscon)

* Tue Sep 08 2015 Michal Luscon <mluscon@redhat.com> 1.1.1-2
- fix access to demands (RhBug:1259194) (Jan Silhan)
- make clean_requiremets_on_remove=True (RhBug:1260280) (Jan Silhan)

* Mon Aug 31 2015 Michal Luscon <mluscon@redhat.com> 1.1.1-1
- Fixed typo (RhBug:1249319) (Adam Salih)
- fixed downgrade with wildcard (RhBug:1234763) (Adam Salih)
- reorganize logic of get_best_selector(s) and query (RhBug:1242946) (Adam
  Salih)
- completion_helper: don't crash if exception occurred (RhBug:1225225) (Igor
  Gnatenko)
- base: expire cache if repo is not available (Michal Luscon)
- Don't suggest --allowerasing if it is enabled (Christian Stadelmann)
- translation works in python3 (RhBug:1254687) (Jan Silhan)
- logrotate less often (RhBug:1247766) (Jan Silhan)
- implement dnf mark command (RhBug:1125925) (Michal Luscon)
- groups: use comps data to migrate persistor (Michal Luscon)
- groups: preserve api compatibility (Michal Luscon)
- groups: use persistor data for removing env/group (Michal Luscon)
- persistor: add migration and bump version (Michal Luscon)
- persistor: store name and ui_name of group (Michal Luscon)
- show real metadata timestamp on the server in verbose mode (Jan Silhan)
- lock: make rpmdb lock blocking (RhBug:1210289) (Michal Luscon)

* Wed Aug 12 2015 Michal Luscon <mluscon@redhat.com> 1.1.0-2
- update: installonly pkgs are not shown in both install and skipped section
  (RhBug:1252415) (Jan Silhan)
- output: sort skipped packages (Jan Silhan)
- output: skipped conflicts are set (RhBug:1252032) (Jan Silhan)
- keep the dwongrading package installed if transaction fails (RhBug:1249379)
  (Jan Silhan)
- don't store empty attributes (RhBug:1246928) (Michael Mraka)
- doc: correct dnf.conf man section (RhBug:1245349) (Michal Luscon)

* Mon Aug 10 2015 Michal Luscon <mluscon@redhat.com> 1.1.0-1
- print skipped pkg with broken deps too (Related:RhBug:1210445) (Jan Silhan)
- history: set commands output as default (RhBug:1218401) (Michal Luscon)
- Update es.po. save:guardar -> save:ahorrar (Máximo Castañeda)
- cosmetic: option arg in Base.*install is replaced with strict (Jan Silhan)
- group: don't fail on first non-existing group (Jan Silhan)
- install: skips local pkgs of lower version when strict=0
  (Related:RhBug:1227952) (Jan Silhan)
- install: skip broken/conflicting packages in groups when strict=0 (Jan
  Silhan)
- install: skip broken/conflicting packages when strict=0 (Jan Silhan)
- implemented `strict` config option working in install cmd (RhBug:1197456)
  (Jan Silhan)
- fixed 'dnf --quiet repolist' lack of output (RhBug:1236310) (Nick Coghlan)
- Add support for MIPS architecture (Michal Toman)
- package: respect baseurl attribute in localPkg() (RhBug:1219638) (Michal
  Luscon)
- Download error message is not written on the same line as progress bar
  anymore (RhBug: 1224248) (Adam Salih)
- dnf downgrade does not try to downgrade not installed packages (RhBug:
  1243501) (max9631)
- pkgs not installed due to rpm error are reported (RhBug:1207981) (Adam Salih)
- dnf install checks availability of all given packages (RhBug:1208918) (Adam
  Salih)
- implemented install_weak_deps config option (RhBug:1221635) (Jan Silhan)
- ignore SIGPIPE (RhBug:1236306) (Michael Mraka)
- always add LoggingTransactionDisplay to the list of transaction displays
  (RhBug:1234639) (Radek Holy)
- Add missing FILES section (RhBug: 1225237) (Adam Salih)
- doc: Add yum vs dnf hook information (RhBug:1244486) (Parag Nemade)
- doc: clarify the expected type of the do_transactions's display parameter
  (Radek Holy)
- apichange: add dnf.cli.demand.DemandSheet.transaction_display (Radek Holy)
- apichange: add dnf.callback.TransactionProgress (Radek Holy)
- move the error output from TransactionDisplay into a separate class (Radek
  Holy)
- rename TransactionDisplay.errorlog to TransactionDisplay.error (Radek Holy)
- report package verification as a regular RPM transaction event (Radek Holy)
- rename TransactionDisplay.event to TransactionDisplay.progress (Radek Holy)
- apichange: deprecate dnf.callback.LoggingTransactionDisplay (Radek Holy)
- use both CliTransactionDisplay and demands.transaction_display (Radek Holy)
- apichange: accept multiple displays in do_transaction (Radek Holy)
- support multiple displays in RPMTransaction (Radek Holy)
