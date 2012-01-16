AC_INIT([texlive-data-ja],[0.0.4])
AM_INIT_AUTOMAKE([no-dist-gzip dist-xz foreign])

dnl http://www.flameeyes.eu/autotools-mythbuster/automake/silent.html
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

dnl TODO: fix autoconf macros used.
AC_PROG_LN_S
m4_ifdef([AC_PROG_MKDIR_P],[AC_PROG_MKDIR_P],[AC_SUBST([MKDIR_P],[mkdir -p])])
m4_ifdef([AC_PROG_SED],[AC_PROG_SED],[AC_SUBST([SED],[sed])])


dnl Enable this if you're using the version of texlive-texmf < 2007-39.
overrides="false"
AC_ARG_ENABLE([overrides],
  [  --enable-overrides  Overrides /usr/share/texmf/web2c/texmf.cnf has bug rhbz"#736242"],
  [case "${enableval}" in
   yes) overrides=true ;;
   no)  overrides=false ;;
   *) AC_MSG_ERROR([bad value ${enableval} for --enable-overrides]) ;;
  esac],[overrides=$overrides])
AM_CONDITIONAL([USE_OVERRIDES],[test x$overrides = xtrue])


AC_CONFIG_FILES([
Makefile
src/Makefile
])

AC_OUTPUT
