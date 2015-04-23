概要
-----

ソースをビルドしてリリース、実際に適用 (アップデート) するまでの全体の流れ:

#. 一応テスト
#. ビルド・リリース用の Source RPM 作成
#. ビルド & リリース (社内 Yum リポジトリへ)
#. 適用 (社内 Yum リポジトリからとってきて普通に yum update -y するだけ)

適用 (デプロイ) 部分は普通の Yum の仕組みを利用しています。設定も可能なものはほとんどすべて .d/ 化していて
yum update -y で適用し、chef/puppet 等新しい仕組みを入れる必要がありません。
それらについては設定の変更は RPM レベルの追加・削除・更新で行うことになります。
(それらについては設定ファイルを直接編集することはまずありません。)

それを実現するため自作の python アプリケーションはこの anyconfig で設定を多層化対応にしてカスタマイズ可能にしています。

詳細: python-anyconfig の例
---------------------------------

以下、python-anyconfig パッケージでのビルド、リリース、適用までの流れの詳細。

まずは /usr/bin/python (python-2.7) でテスト。
(もちろん `github <https://github.com/ssato/python-anyconfig>`_ で CI してます; この一連のテストは本来的には不要)

.. code-block:: console

  ssato@localhost% rpm -qf =python
  python-2.7.8-8.fc21.x86_64
  ssato@localhost% ./pkg/runtest.sh
  Creating output dir as it's not found: /tmp/python-anyconfig-tests-AOnBR3/dumpdir
  <traceback object at 0x7f365583eef0>
  Doctest: anyconfig.backend.backends.fst ... ok
  Doctest: anyconfig.backend.backends.snd ... ok
  Doctest: anyconfig.backend.backends.uniq ... ok
  Doctest: anyconfig.backend.base.mk_opt_args ... ok
  Doctest: anyconfig.backend.ini_._parse ... ok
  test_10_find_by_file (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_20_find_by_type (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_30_list_types (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_40_cmp_cps (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_10_set_container (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_10_type (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_10_type__force_set (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_20__load__ignore_missing (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_50_dumps_impl (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_50_load_impl (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_10_mk_dump_dir_if_not_exist (anyconfig.backend.tests.base.Test_10_effectful_functions) ... ok
  test_00_supports (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_10_loads (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_20_load (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_20_load__w_options (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_30_dumps (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_should_show_error_on_invalid_ini (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_00_supports (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_10_loads (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_20_load (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_20_load__optional_kwargs (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_30_dumps (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_50_dump_w_backend_specific_options (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_00 (anyconfig.backend.tests.noyaml.Test_YamlConfigParser) ... ok
  test_10_load (anyconfig.backend.tests.noyaml.Test_YamlConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.noyaml.Test_YamlConfigParser) ... ok
  test_00 (anyconfig.backend.tests.nojson.Test_00_JsonConfigParser) ... ok
  test_10_load (anyconfig.backend.tests.nojson.Test_00_JsonConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.nojson.Test_00_JsonConfigParser) ... ok
  test_00_supports (anyconfig.backend.tests.xml_.Test_XmlConfigParser) ... ok
  FIXME: Implement test cases for XmlConfigParser.loads ... ok
  FIXME: Implement test cases for XmlConfigParser.load ... ok
  test_30_dumps_impl (anyconfig.backend.tests.xml_.Test_XmlConfigParser) ... ok
  Doctest: anyconfig.compat._from_iterable ... ok
  Doctest: anyconfig.compat.copen ... ok
  Doctest: anyconfig.compat.iteritems ... ok
  Doctest: anyconfig.compat.py3_cmp ... ok
  Doctest: anyconfig.compat.py3_iteritems ... ok
  Doctest: anyconfig.mergeabledict.MergeableDict.update_w_merge ... ok
  Doctest: anyconfig.mergeabledict.MergeableDict.update_w_replace ... ok
  Doctest: anyconfig.mergeabledict.MergeableDict.update_wo_replace ... ok
  Doctest: anyconfig.mergeabledict._mk_nested_dic ... ok
  Doctest: anyconfig.mergeabledict.get ... ok
  Doctest: anyconfig.mergeabledict.is_mergeabledict_or_dict ... ok
  Doctest: anyconfig.mergeabledict.set_ ... ok
  Doctest: anyconfig.parser.parse_attrlist ... ok
  Doctest: anyconfig.parser.parse_attrlist_0 ... ok
  Doctest: anyconfig.parser.parse_list ... ok
  Doctest: anyconfig.parser.parse_path ... ok
  Doctest: anyconfig.parser.parse_single ... ok
  test_00_supports (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_10_loads (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_12_loads__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_20_load (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_20_load__w_options (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_22_load__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_30_dumps (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_32_dumps__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_40_dump__w_options (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_42_dump__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  Doctest: anyconfig.template.make_template_paths ... ok
  Doctest: anyconfig.template.render_s ... ok
  Doctest: anyconfig.utils.concat ... ok
  Doctest: anyconfig.utils.get_file_extension ... ok
  Doctest: anyconfig.utils.is_iterable ... ok
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-qjO4V7/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-qjO4V7/a.json
  Using config parser of type: ini
  Using config parser of type: json
  Using config parser of type: json
  Using config parser of type: yaml
  Using config parser of type: xml
  Dumping: /tmp/python-anyconfig-tests-Njpw6l/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-Njpw6l/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-_ivBwV/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-_ivBwV/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-_ivBwV/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-_ivBwV/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-_ivBwV/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-_ivBwV/b.json
  No parser found for given file: dummy.ext_not_exist
  Using config parser of type: ini
  Loading: ./conf_file_should_not_exist
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-hYgVEh/a.yaml
  Compiling: /tmp/python-anyconfig-tests-hYgVEh/a.yaml
  test_10_dump_and_load (anyconfig.tests.00.Test_10_effectful_functions) ... ok
  test_20_dump_and_multi_load (anyconfig.tests.00.Test_10_effectful_functions) ... ok
  test_10_find_loader__w_forced_type (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_12_find_loader__w_forced_type__none (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_20_find_loader__by_file (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_22_find_loader__by_file__none (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_30_dumps_and_loads (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_30_dumps_and_loads__w_options (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_32_dumps_and_loads__w_options__no_dumper (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_40_loads_wo_type (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_42_loads_w_type_not_exist (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_44_loads_w_type__template (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_46_loads_w_type__broken_template (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_00___init__ (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  test_10_find_module (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  test_20_load_module__basename (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  test_22_load_module__fullname (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  TODO: Implement it correctly and add a test case. ... ok
  test_00 (anyconfig.tests.globals.Test_00) ... ok
  test_00 (anyconfig.tests.init.Test_00) ... ok
  test_create_from__convert_to (anyconfig.tests.mergeabledict.Test_00_utility_functions) ... ok
  test_update__w_None (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_merge_dicts (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_merge_dicts_and_lists (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_replace (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_replace__not_a_dict (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__wo_replace (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_00_parse_single (anyconfig.tests.parser.Test_00_parse) ... ok
  test_10_parse_list (anyconfig.tests.parser.Test_00_parse) ... ok
  test_20_parse_attrlist_0 (anyconfig.tests.parser.Test_00_parse) ... ok
  test_30_parse (anyconfig.tests.parser.Test_00_parse) ... ok
  test_50_parse_path__empty (anyconfig.tests.parser.Test_00_parse) ... ok
  test_52_parse_path__single (anyconfig.tests.parser.Test_00_parse) ... ok
  test_54_parse_path__multi (anyconfig.tests.parser.Test_00_parse) ... ok
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-kyN37u/a.yml
  Compiling: /tmp/python-anyconfig-tests-kyN37u/a.yml
  test_00_run_script (anyconfig.tests.lib.Test_00) ... ok
  test_00_get_file_extension (anyconfig.tests.utils.Test_functions) ... ok
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-zrs06e/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-zrs06e/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-zrs06e/b.json
  Using config parser of type: ini
  Loading: ./conf_file_should_not_exist
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-hpWzzD/a.yml
  Compiling: /tmp/python-anyconfig-tests-hpWzzD/a.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-hpWzzD/b.yml
  Compiling: /tmp/python-anyconfig-tests-hpWzzD/b.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-hpWzzD/a.yml
  Compiling: /tmp/python-anyconfig-tests-hpWzzD/a.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-hpWzzD/b.yml
  Compiling: /tmp/python-anyconfig-tests-hpWzzD/b.yml
  test_10_render_impl__wo_paths (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_12_render_impl__w_paths (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_20_render__wo_paths (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_22_render__w_wrong_template_path (anyconfig.tests.template.Test_20_render_templates) ... ok
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-hpWzzD/b.yml
  Compiling: /tmp/python-anyconfig-tests-hpWzzD/b.yml
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-C0pEhf/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-C0pEhf/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-C0pEhf/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-C0pEhf/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-C0pEhf/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-C0pEhf/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-C0pEhf/b.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-D33F2l/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-D33F2l/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-D33F2l/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-D33F2l/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-D33F2l/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-D33F2l/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-D33F2l/b.json
  Using config parser of type: ini
  Loading: ./conf_file_should_not_exist
  test_10_dump_and_single_load (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_12_dump_and_single_load__no_parser (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_14_single_load__ignore_missing (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_16_single_load__template (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_18_single_load__templates (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_20_dump_and_multi_load (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_22_multi_load__ignore_missing (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_24_multi_load__templates (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_30_dump_and_load (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_32_dump_and_load__w_options (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_34_load__ignore_missing (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  Usage: nosetests [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

  Examples:
    nosetests --list
    nosetests -I yaml -O yaml /etc/xyz/conf.d/a.conf
    nosetests -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
    nosetests '/etc/xyz/conf.d/*.json' -o xyz.yml \
      --atype json -A '{"obsoletes": "sysdata", "conflicts": "sysdata-old"}'
    nosetests '/etc/xyz/conf.d/*.json' -o xyz.yml \
      -A obsoletes:sysdata;conflicts:sysdata-old
    nosetests /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
    nosetests '/etc/foo.d/*.json' -M noreplace
    nosetests '/etc/foo.d/*.json' --get a.b.c
    nosetests '/etc/foo.d/*.json' --set a.b.c=1

  nosetests: error: no such option: --wrong-option-xyz
  Dumping: /tmp/python-anyconfig-tests-BE7KRm/a.json
  Loading: /tmp/python-anyconfig-tests-BE7KRm/a.json
  Dumping: /tmp/python-anyconfig-tests-ig_7Fq/a.json
  Loading: /tmp/python-anyconfig-tests-ig_7Fq/a.json
  Loading: /tmp/python-anyconfig-tests-ig_7Fq/b.json
  Dumping: /tmp/python-anyconfig-tests-gz4TO0/a.json
  Loading: /tmp/python-anyconfig-tests-gz4TO0/a.json
  Loading: /tmp/python-anyconfig-tests-gz4TO0/b.json
  Loading: ./conf_file_should_not_exist.json
  Dumping: /tmp/python-anyconfig-tests-UDsg6V/a0.json
  Dumping: /tmp/python-anyconfig-tests-UDsg6V/a1.json
  Loading: /tmp/python-anyconfig-tests-UDsg6V/a0.json
  Loading: /tmp/python-anyconfig-tests-UDsg6V/a1.json
  Dumping: /tmp/python-anyconfig-tests-VUKe3e/a.json
  Loading: /tmp/python-anyconfig-tests-VUKe3e/a.json
  Loading: /tmp/python-anyconfig-tests-VUKe3e/b.json
  Dumping: /tmp/python-anyconfig-tests-3JB6WB/a.json
  Loading: /tmp/python-anyconfig-tests-3JB6WB/a.json
  Dumping: /tmp/python-anyconfig-tests-bK_OeL/a.json
  Loading: /tmp/python-anyconfig-tests-bK_OeL/a.json
  Dumping: /tmp/python-anyconfig-tests-bUR4l_/in/a0.yml
  Loading: /tmp/python-anyconfig-tests-bUR4l_/in/a0.yml
  Loading: /tmp/python-anyconfig-tests-bUR4l_/in/a1.yml
  Dumping: /tmp/python-anyconfig-tests-6s3JXz/a.json
  Loading: /tmp/python-anyconfig-tests-6s3JXz/a.json
  Loading: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/anyconfig/tests/00-template-ctx.yml
  Loading: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/anyconfig/tests/10-template-config.yml
  Dumping: /tmp/python-anyconfig-tests-56lOz2/a.json
  Loading: /tmp/python-anyconfig-tests-56lOz2/a.json
  No parser found for given file: out.txt
  No parser found for given file: in.txt
  No parser found for given file: out.txt
  No parser found for given file: /dev/null
  Loading: /tmp/python-anyconfig-tests-zzhs1u/out.yml
  test_10__show_usage (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_12__wrong_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_20__list (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_22__list (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_30_single_input (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_32_single_input_w_get_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_34_single_input_w_set_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_36_single_input__ignore_missing (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_40_multiple_inputs (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_50_single_input__w_arg_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_60_output_wo_output_option_w_otype (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_62_output_wo_output_option_and_otype_w_itype (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_70_multi_inputs__w_template (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_72_single_input__no_template (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_74_multi_inputs__w_template (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_80_no_out_dumper (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_82_no_itype_and_otype (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_90_no_inputs__w_env_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok

  ----------------------------------------------------------------------
  Ran 142 tests in 0.801s

  OK

続いて tox で python-2.7/3.4 でも一応テスト。

.. code-block:: console

  ssato@localhost% tox            ~/repos/public/github.com/ssato/python-anyconfig.git
  GLOB sdist-make: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/setup.py
  py27 inst-nodeps: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/.tox/dist/anyconfig-0.0.7.zip
  py27 runtests: PYTHONHASHSEED='4118719510'
  py27 runtests: commands[0] | bash pkg/runtest.sh
  Creating output dir as it's not found: /tmp/python-anyconfig-tests-rJqetv/dumpdir
  <traceback object at 0x7f924d4c8dd0>
  Doctest: anyconfig.backend.backends.fst ... ok
  Doctest: anyconfig.backend.backends.snd ... ok
  Doctest: anyconfig.backend.backends.uniq ... ok
  Doctest: anyconfig.backend.base.mk_opt_args ... ok
  Doctest: anyconfig.backend.ini_._parse ... ok
  test_10_find_by_file (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_20_find_by_type (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_30_list_types (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_40_cmp_cps (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_10_set_container (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_10_type (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_10_type__force_set (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_20__load__ignore_missing (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_50_dumps_impl (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_50_load_impl (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_00_supports (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_10_loads (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_20_load (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_20_load__w_options (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_30_dumps (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_should_show_error_on_invalid_ini (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_10_mk_dump_dir_if_not_exist (anyconfig.backend.tests.base.Test_10_effectful_functions) ... ok
  test_00 (anyconfig.backend.tests.nojson.Test_00_JsonConfigParser) ... ok
  test_10_load (anyconfig.backend.tests.nojson.Test_00_JsonConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.nojson.Test_00_JsonConfigParser) ... ok
  test_00 (anyconfig.backend.tests.noyaml.Test_YamlConfigParser) ... ok
  test_10_load (anyconfig.backend.tests.noyaml.Test_YamlConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.noyaml.Test_YamlConfigParser) ... ok
  test_00_supports (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_10_loads (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_20_load (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_20_load__optional_kwargs (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_30_dumps (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_50_dump_w_backend_specific_options (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_00_supports (anyconfig.backend.tests.xml_.Test_XmlConfigParser) ... ok
  FIXME: Implement test cases for XmlConfigParser.loads ... ok
  FIXME: Implement test cases for XmlConfigParser.load ... ok
  test_30_dumps_impl (anyconfig.backend.tests.xml_.Test_XmlConfigParser) ... ok
  Doctest: anyconfig.compat._from_iterable ... ok
  Doctest: anyconfig.compat.copen ... ok
  Doctest: anyconfig.compat.iteritems ... ok
  Doctest: anyconfig.compat.py3_cmp ... ok
  Doctest: anyconfig.compat.py3_iteritems ... ok
  Doctest: anyconfig.mergeabledict.MergeableDict.update_w_merge ... ok
  Doctest: anyconfig.mergeabledict.MergeableDict.update_w_replace ... ok
  Doctest: anyconfig.mergeabledict.MergeableDict.update_wo_replace ... ok
  Doctest: anyconfig.mergeabledict._mk_nested_dic ... ok
  Doctest: anyconfig.mergeabledict.get ... ok
  Doctest: anyconfig.mergeabledict.is_mergeabledict_or_dict ... ok
  Doctest: anyconfig.mergeabledict.set_ ... ok
  Doctest: anyconfig.parser.parse_attrlist ... ok
  Doctest: anyconfig.parser.parse_attrlist_0 ... ok
  Doctest: anyconfig.parser.parse_list ... ok
  Doctest: anyconfig.parser.parse_path ... ok
  Doctest: anyconfig.parser.parse_single ... ok
  test_00_supports (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_10_loads (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_12_loads__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_20_load (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_20_load__w_options (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_22_load__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_30_dumps (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_32_dumps__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_40_dump__w_options (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_42_dump__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  Doctest: anyconfig.template.make_template_paths ... ok
  Doctest: anyconfig.template.render_s ... ok
  Doctest: anyconfig.utils.concat ... ok
  Doctest: anyconfig.utils.get_file_extension ... ok
  Doctest: anyconfig.utils.is_iterable ... ok
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-GXfnrE/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-GXfnrE/a.json
  Using config parser of type: ini
  Using config parser of type: json
  Using config parser of type: yaml
  Using config parser of type: xml
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-8AqAKc/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-8AqAKc/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-8AqAKc/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-8AqAKc/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-8AqAKc/a.json
  Using config parser of type: json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-9yT5bR/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-9yT5bR/a.json
  Loading: /tmp/python-anyconfig-tests-8AqAKc/b.json
  No parser found for given file: dummy.ext_not_exist
  Using config parser of type: ini
  Loading: ./conf_file_should_not_exist
  test_10_find_loader__w_forced_type (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_12_find_loader__w_forced_type__none (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_20_find_loader__by_file (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_22_find_loader__by_file__none (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_30_dumps_and_loads (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_30_dumps_and_loads__w_options (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_32_dumps_and_loads__w_options__no_dumper (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_40_loads_wo_type (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_42_loads_w_type_not_exist (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_44_loads_w_type__template (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_46_loads_w_type__broken_template (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_10_dump_and_load (anyconfig.tests.00.Test_10_effectful_functions) ... ok
  test_20_dump_and_multi_load (anyconfig.tests.00.Test_10_effectful_functions) ... ok
  test_00___init__ (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  test_10_find_module (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  test_20_load_module__basename (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  test_22_load_module__fullname (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  TODO: Implement it correctly and add a test case. ... ok
  test_00 (anyconfig.tests.globals.Test_00) ... ok
  test_00 (anyconfig.tests.init.Test_00) ... ok
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-7feDA_/a.yaml
  Compiling: /tmp/python-anyconfig-tests-7feDA_/a.yaml
  test_create_from__convert_to (anyconfig.tests.mergeabledict.Test_00_utility_functions) ... ok
  test_update__w_None (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_merge_dicts (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_merge_dicts_and_lists (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_replace (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_replace__not_a_dict (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__wo_replace (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-odvZHc/a.yml
  Compiling: /tmp/python-anyconfig-tests-odvZHc/a.yml
  test_00_parse_single (anyconfig.tests.parser.Test_00_parse) ... ok
  test_10_parse_list (anyconfig.tests.parser.Test_00_parse) ... ok
  test_20_parse_attrlist_0 (anyconfig.tests.parser.Test_00_parse) ... ok
  test_30_parse (anyconfig.tests.parser.Test_00_parse) ... ok
  test_50_parse_path__empty (anyconfig.tests.parser.Test_00_parse) ... ok
  test_52_parse_path__single (anyconfig.tests.parser.Test_00_parse) ... ok
  test_54_parse_path__multi (anyconfig.tests.parser.Test_00_parse) ... ok
  test_00_run_script (anyconfig.tests.lib.Test_00) ... ok
  test_00_get_file_extension (anyconfig.tests.utils.Test_functions) ... ok
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-ZQmnOr/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-ZQmnOr/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-ZQmnOr/b.json
  Using config parser of type: ini
  Loading: ./conf_file_should_not_exist
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-2B5p2O/a.yml
  Compiling: /tmp/python-anyconfig-tests-2B5p2O/a.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-2B5p2O/b.yml
  Compiling: /tmp/python-anyconfig-tests-2B5p2O/b.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-2B5p2O/a.yml
  Compiling: /tmp/python-anyconfig-tests-2B5p2O/a.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-2B5p2O/b.yml
  Compiling: /tmp/python-anyconfig-tests-2B5p2O/b.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-2B5p2O/b.yml
  Compiling: /tmp/python-anyconfig-tests-2B5p2O/b.yml
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-LWwnGN/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-LWwnGN/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-LWwnGN/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-LWwnGN/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-LWwnGN/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-LWwnGN/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-LWwnGN/b.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-2kgrhE/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-2kgrhE/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-2kgrhE/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-2kgrhE/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-2kgrhE/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-2kgrhE/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-2kgrhE/b.json
  Using config parser of type: ini
  Loading: ./conf_file_should_not_exist
  test_10_render_impl__wo_paths (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_12_render_impl__w_paths (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_20_render__wo_paths (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_22_render__w_wrong_template_path (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_10_dump_and_single_load (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_12_dump_and_single_load__no_parser (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_14_single_load__ignore_missing (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_16_single_load__template (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_18_single_load__templates (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_20_dump_and_multi_load (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_22_multi_load__ignore_missing (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_24_multi_load__templates (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_30_dump_and_load (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_32_dump_and_load__w_options (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_34_load__ignore_missing (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  Usage: nosetests [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

  Examples:
    nosetests --list
    nosetests -I yaml -O yaml /etc/xyz/conf.d/a.conf
    nosetests -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
    nosetests '/etc/xyz/conf.d/*.json' -o xyz.yml \
      --atype json -A '{"obsoletes": "sysdata", "conflicts": "sysdata-old"}'
    nosetests '/etc/xyz/conf.d/*.json' -o xyz.yml \
      -A obsoletes:sysdata;conflicts:sysdata-old
    nosetests /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
    nosetests '/etc/foo.d/*.json' -M noreplace
    nosetests '/etc/foo.d/*.json' --get a.b.c
    nosetests '/etc/foo.d/*.json' --set a.b.c=1

  nosetests: error: no such option: --wrong-option-xyz
  Dumping: /tmp/python-anyconfig-tests-934tCI/a.json
  Loading: /tmp/python-anyconfig-tests-934tCI/a.json
  Dumping: /tmp/python-anyconfig-tests-uNfUjb/a.json
  Loading: /tmp/python-anyconfig-tests-uNfUjb/a.json
  Loading: /tmp/python-anyconfig-tests-uNfUjb/b.json
  Dumping: /tmp/python-anyconfig-tests-rzreXq/a.json
  Loading: /tmp/python-anyconfig-tests-rzreXq/a.json
  Loading: /tmp/python-anyconfig-tests-rzreXq/b.json
  Loading: ./conf_file_should_not_exist.json
  Dumping: /tmp/python-anyconfig-tests-zwXtFA/a0.json
  Dumping: /tmp/python-anyconfig-tests-zwXtFA/a1.json
  Loading: /tmp/python-anyconfig-tests-zwXtFA/a0.json
  Loading: /tmp/python-anyconfig-tests-zwXtFA/a1.json
  Dumping: /tmp/python-anyconfig-tests-b77vz9/a.json
  Loading: /tmp/python-anyconfig-tests-b77vz9/a.json
  Loading: /tmp/python-anyconfig-tests-b77vz9/b.json
  Dumping: /tmp/python-anyconfig-tests-90AMP1/a.json
  Loading: /tmp/python-anyconfig-tests-90AMP1/a.json
  Dumping: /tmp/python-anyconfig-tests-i_Effu/a.json
  Loading: /tmp/python-anyconfig-tests-i_Effu/a.json
  Dumping: /tmp/python-anyconfig-tests-2YYh1O/in/a0.yml
  Loading: /tmp/python-anyconfig-tests-2YYh1O/in/a0.yml
  Loading: /tmp/python-anyconfig-tests-2YYh1O/in/a1.yml
  Dumping: /tmp/python-anyconfig-tests-5ccu1e/a.json
  Loading: /tmp/python-anyconfig-tests-5ccu1e/a.json
  Loading: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/anyconfig/tests/00-template-ctx.yml
  Loading: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/anyconfig/tests/10-template-config.yml
  Dumping: /tmp/python-anyconfig-tests-NhW8NP/a.json
  Loading: /tmp/python-anyconfig-tests-NhW8NP/a.json
  No parser found for given file: out.txt
  No parser found for given file: in.txt
  No parser found for given file: out.txt
  No parser found for given file: /dev/null
  Loading: /tmp/python-anyconfig-tests-9VOyJA/out.yml
  test_10__show_usage (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_12__wrong_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_20__list (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_22__list (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_30_single_input (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_32_single_input_w_get_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_34_single_input_w_set_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_36_single_input__ignore_missing (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_40_multiple_inputs (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_50_single_input__w_arg_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_60_output_wo_output_option_w_otype (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_62_output_wo_output_option_and_otype_w_itype (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_70_multi_inputs__w_template (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_72_single_input__no_template (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_74_multi_inputs__w_template (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_80_no_out_dumper (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_82_no_itype_and_otype (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_90_no_inputs__w_env_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok

  ----------------------------------------------------------------------
  Ran 142 tests in 0.701s

  OK
  py34 inst-nodeps: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/.tox/dist/anyconfig-0.0.7.zip
  py34 runtests: PYTHONHASHSEED='4118719510'
  py34 runtests: commands[0] | bash pkg/runtest.sh
  Creating output dir as it's not found: /tmp/python-anyconfig-tests-o0h30zmu/dumpdir
  Doctest: anyconfig.backend.backends.fst ... ok
  Doctest: anyconfig.backend.backends.snd ... ok
  Doctest: anyconfig.backend.backends.uniq ... ok
  Doctest: anyconfig.backend.base.mk_opt_args ... ok
  Doctest: anyconfig.backend.ini_._parse ... ok
  test_10_find_by_file (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_20_find_by_type (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_30_list_types (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  test_40_cmp_cps (anyconfig.backend.tests.backends.Test_00_pure_functions) ... ok
  <traceback object at 0x7f1e08694f48>
  test_10_mk_dump_dir_if_not_exist (anyconfig.backend.tests.base.Test_10_effectful_functions) ... ok
  test_10_set_container (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_10_type (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_10_type__force_set (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_20__load__ignore_missing (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_50_dumps_impl (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_50_load_impl (anyconfig.backend.tests.base.Test_00_ConfigParser) ... ok
  test_00_supports (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_10_loads (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_20_load (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_20_load__w_options (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_30_dumps (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_should_show_error_on_invalid_ini (anyconfig.backend.tests.ini_.Test_IniConfigParser) ... ok
  test_00_supports (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_10_loads (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_20_load (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_20_load__optional_kwargs (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_30_dumps (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_50_dump_w_backend_specific_options (anyconfig.backend.tests.json_.Test_JsonConfigParser) ... ok
  test_00 (anyconfig.backend.tests.nojson.Test_00_JsonConfigParser) ... ok
  test_10_load (anyconfig.backend.tests.nojson.Test_00_JsonConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.nojson.Test_00_JsonConfigParser) ... ok
  test_00 (anyconfig.backend.tests.noyaml.Test_YamlConfigParser) ... ok
  test_10_load (anyconfig.backend.tests.noyaml.Test_YamlConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.noyaml.Test_YamlConfigParser) ... ok
  test_00_supports (anyconfig.backend.tests.xml_.Test_XmlConfigParser) ... ok
  FIXME: Implement test cases for XmlConfigParser.loads ... ok
  FIXME: Implement test cases for XmlConfigParser.load ... ok
  test_30_dumps_impl (anyconfig.backend.tests.xml_.Test_XmlConfigParser) ... ok
  Doctest: anyconfig.compat._from_iterable ... ok
  Doctest: anyconfig.compat.cmp ... ok
  Doctest: anyconfig.compat.copen ... ok
  Doctest: anyconfig.compat.py3_iteritems ... ok
  Doctest: anyconfig.parser.parse_attrlist ... ok
  Doctest: anyconfig.parser.parse_attrlist_0 ... ok
  Doctest: anyconfig.parser.parse_list ... ok
  Doctest: anyconfig.parser.parse_path ... ok
  Doctest: anyconfig.parser.parse_single ... ok
  Doctest: anyconfig.mergeabledict.MergeableDict.update_w_merge ... ok
  Doctest: anyconfig.mergeabledict.MergeableDict.update_w_replace ... ok
  Doctest: anyconfig.mergeabledict.MergeableDict.update_wo_replace ... ok
  Doctest: anyconfig.mergeabledict._mk_nested_dic ... ok
  Doctest: anyconfig.mergeabledict.get ... ok
  Doctest: anyconfig.mergeabledict.is_mergeabledict_or_dict ... ok
  Doctest: anyconfig.mergeabledict.set_ ... ok
  Doctest: anyconfig.template.make_template_paths ... ok
  Doctest: anyconfig.template.render_s ... ok
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-hqnrvope/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-hqnrvope/a.json
  Doctest: anyconfig.utils.concat ... ok
  Doctest: anyconfig.utils.get_file_extension ... ok
  Doctest: anyconfig.utils.is_iterable ... ok
  Using config parser of type: ini
  Using config parser of type: json
  Using config parser of type: yaml
  Using config parser of type: xml
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-eved9byp/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-eved9byp/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-6dp19k3o/a.json
  test_00_supports (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_10_loads (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_12_loads__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_20_load (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_20_load__w_options (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_22_load__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_30_dumps (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_32_dumps__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_40_dump (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_40_dump__w_options (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  test_42_dump__safe (anyconfig.backend.tests.yaml_.Test_YamlConfigParser) ... ok
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-6dp19k3o/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-6dp19k3o/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-6dp19k3o/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-6dp19k3o/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-6dp19k3o/b.json
  No parser found for given file: dummy.ext_not_exist
  Using config parser of type: ini
  Loading: ./conf_file_should_not_exist
  test_10_dump_and_load (anyconfig.tests.00.Test_10_effectful_functions) ... ok
  test_20_dump_and_multi_load (anyconfig.tests.00.Test_10_effectful_functions) ... ok
  test_10_find_loader__w_forced_type (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_12_find_loader__w_forced_type__none (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_20_find_loader__by_file (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_22_find_loader__by_file__none (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_30_dumps_and_loads (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_30_dumps_and_loads__w_options (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_32_dumps_and_loads__w_options__no_dumper (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_40_loads_wo_type (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_42_loads_w_type_not_exist (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_44_loads_w_type__template (anyconfig.tests.api.Test_10_pure_functions) ... ok
  test_46_loads_w_type__broken_template (anyconfig.tests.api.Test_10_pure_functions) ... ok
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-i_o2milo/a.yaml
  Compiling: /tmp/python-anyconfig-tests-i_o2milo/a.yaml
  test_00 (anyconfig.tests.globals.Test_00) ... ok
  test_00 (anyconfig.tests.init.Test_00) ... ok
  test_00___init__ (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  test_10_find_module (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  test_20_load_module__basename (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  test_22_load_module__fullname (anyconfig.tests.common.Test_00_MaskedImportLoader) ... ok
  TODO: Implement it correctly and add a test case. ... ok
  test_create_from__convert_to (anyconfig.tests.mergeabledict.Test_00_utility_functions) ... ok
  test_update__w_None (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_merge_dicts (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_merge_dicts_and_lists (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_replace (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__w_replace__not_a_dict (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_update__wo_replace (anyconfig.tests.mergeabledict.Test_10_MergeableDict) ... ok
  test_00_parse_single (anyconfig.tests.parser.Test_00_parse) ... ok
  test_10_parse_list (anyconfig.tests.parser.Test_00_parse) ... ok
  test_20_parse_attrlist_0 (anyconfig.tests.parser.Test_00_parse) ... ok
  test_30_parse (anyconfig.tests.parser.Test_00_parse) ... ok
  test_50_parse_path__empty (anyconfig.tests.parser.Test_00_parse) ... ok
  test_52_parse_path__single (anyconfig.tests.parser.Test_00_parse) ... ok
  test_54_parse_path__multi (anyconfig.tests.parser.Test_00_parse) ... ok
  test_00_run_script (anyconfig.tests.lib.Test_00) ... ok
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-dtktoel4/a.yml
  Compiling: /tmp/python-anyconfig-tests-dtktoel4/a.yml
  test_00_get_file_extension (anyconfig.tests.utils.Test_functions) ... ok
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-mbo7msqt/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-mbo7msqt/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-mbo7msqt/b.json
  Using config parser of type: ini
  Loading: ./conf_file_should_not_exist
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-_vptor55/a.yml
  Compiling: /tmp/python-anyconfig-tests-_vptor55/a.yml
  test_10_render_impl__wo_paths (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_12_render_impl__w_paths (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_20_render__wo_paths (anyconfig.tests.template.Test_20_render_templates) ... ok
  test_22_render__w_wrong_template_path (anyconfig.tests.template.Test_20_render_templates) ... ok
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-_vptor55/b.yml
  Compiling: /tmp/python-anyconfig-tests-_vptor55/b.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-_vptor55/a.yml
  Compiling: /tmp/python-anyconfig-tests-_vptor55/a.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-_vptor55/b.yml
  Compiling: /tmp/python-anyconfig-tests-_vptor55/b.yml
  Using config parser of type: yaml
  Loading: /tmp/python-anyconfig-tests-_vptor55/b.yml
  Compiling: /tmp/python-anyconfig-tests-_vptor55/b.yml
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-by8cyx9q/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-by8cyx9q/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-by8cyx9q/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-by8cyx9q/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-by8cyx9q/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-by8cyx9q/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-by8cyx9q/b.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-m38_mwl6/a.json
  Using config parser of type: json
  Dumping: /tmp/python-anyconfig-tests-m38_mwl6/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-m38_mwl6/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-m38_mwl6/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-m38_mwl6/b.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-m38_mwl6/a.json
  Using config parser of type: json
  Loading: /tmp/python-anyconfig-tests-m38_mwl6/b.json
  Using config parser of type: ini
  Loading: ./conf_file_should_not_exist
  test_10_dump_and_single_load (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_12_dump_and_single_load__no_parser (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_14_single_load__ignore_missing (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_16_single_load__template (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_18_single_load__templates (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_20_dump_and_multi_load (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_22_multi_load__ignore_missing (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_24_multi_load__templates (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_30_dump_and_load (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_32_dump_and_load__w_options (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  test_34_load__ignore_missing (anyconfig.tests.api.Test_20_effectful_functions) ... ok
  Usage: nosetests [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

  Examples:
    nosetests --list
    nosetests -I yaml -O yaml /etc/xyz/conf.d/a.conf
    nosetests -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
    nosetests '/etc/xyz/conf.d/*.json' -o xyz.yml \
      --atype json -A '{"obsoletes": "sysdata", "conflicts": "sysdata-old"}'
    nosetests '/etc/xyz/conf.d/*.json' -o xyz.yml \
      -A obsoletes:sysdata;conflicts:sysdata-old
    nosetests /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
    nosetests '/etc/foo.d/*.json' -M noreplace
    nosetests '/etc/foo.d/*.json' --get a.b.c
    nosetests '/etc/foo.d/*.json' --set a.b.c=1

  nosetests: error: no such option: --wrong-option-xyz
  Dumping: /tmp/python-anyconfig-tests-j7n_33oc/a.json
  Loading: /tmp/python-anyconfig-tests-j7n_33oc/a.json
  Dumping: /tmp/python-anyconfig-tests-7qlvf30n/a.json
  Loading: /tmp/python-anyconfig-tests-7qlvf30n/a.json
  Loading: /tmp/python-anyconfig-tests-7qlvf30n/b.json
  Dumping: /tmp/python-anyconfig-tests-qucczuwi/a.json
  Loading: /tmp/python-anyconfig-tests-qucczuwi/a.json
  Loading: /tmp/python-anyconfig-tests-qucczuwi/b.json
  Loading: ./conf_file_should_not_exist.json
  Dumping: /tmp/python-anyconfig-tests-0w640mbz/a0.json
  Dumping: /tmp/python-anyconfig-tests-0w640mbz/a1.json
  Loading: /tmp/python-anyconfig-tests-0w640mbz/a0.json
  Loading: /tmp/python-anyconfig-tests-0w640mbz/a1.json
  Dumping: /tmp/python-anyconfig-tests-4g5puj42/a.json
  Loading: /tmp/python-anyconfig-tests-4g5puj42/a.json
  Loading: /tmp/python-anyconfig-tests-4g5puj42/b.json
  Dumping: /tmp/python-anyconfig-tests-zbv7zran/a.json
  Loading: /tmp/python-anyconfig-tests-zbv7zran/a.json
  Dumping: /tmp/python-anyconfig-tests-szc68qlf/a.json
  Loading: /tmp/python-anyconfig-tests-szc68qlf/a.json
  Dumping: /tmp/python-anyconfig-tests-pgcyojwy/in/a0.yml
  Loading: /tmp/python-anyconfig-tests-pgcyojwy/in/a0.yml
  Loading: /tmp/python-anyconfig-tests-pgcyojwy/in/a1.yml
  Dumping: /tmp/python-anyconfig-tests-apoakt5u/a.json
  Loading: /tmp/python-anyconfig-tests-apoakt5u/a.json
  Loading: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/anyconfig/tests/00-template-ctx.yml
  Loading: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/anyconfig/tests/10-template-config.yml
  Dumping: /tmp/python-anyconfig-tests-7e_3hzz5/a.json
  Loading: /tmp/python-anyconfig-tests-7e_3hzz5/a.json
  No parser found for given file: out.txt
  No parser found for given file: in.txt
  No parser found for given file: out.txt
  No parser found for given file: /dev/null
  Loading: /tmp/python-anyconfig-tests-dzu7elyo/out.yml
  test_10__show_usage (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_12__wrong_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_20__list (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_22__list (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_30_single_input (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_32_single_input_w_get_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_34_single_input_w_set_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_36_single_input__ignore_missing (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_40_multiple_inputs (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_50_single_input__w_arg_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_60_output_wo_output_option_w_otype (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_62_output_wo_output_option_and_otype_w_itype (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_70_multi_inputs__w_template (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_72_single_input__no_template (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_74_multi_inputs__w_template (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_80_no_out_dumper (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_82_no_itype_and_otype (anyconfig.tests.cli.Test_10_effectful_functions) ... ok
  test_90_no_inputs__w_env_option (anyconfig.tests.cli.Test_10_effectful_functions) ... ok

  ----------------------------------------------------------------------
  Ran 141 tests in 0.983s

  OK
  ______________________________________ summary ______________________________________
    py27: commands succeeded
    py34: commands succeeded
    congratulations :)
  ssato@localhost% ls             ~/repos/public/github.com/ssato/python-anyconfig.git

これからビルド、リリースのためにまず Source RPM をビルド。
(このできた Source RPM をそのまま配布するわけではない)

.. code-block:: console

  ssato@localhost% python setup.py srpm
  running srpm
  running sdist
  running egg_info
  writing anyconfig.egg-info/PKG-INFO
  writing top-level names to anyconfig.egg-info/top_level.txt
  writing dependency_links to anyconfig.egg-info/dependency_links.txt
  writing entry points to anyconfig.egg-info/entry_points.txt
  reading manifest file 'anyconfig.egg-info/SOURCES.txt'
  reading manifest template 'MANIFEST.in'
  writing manifest file 'anyconfig.egg-info/SOURCES.txt'
  running check
  creating anyconfig-0.0.7
  creating anyconfig-0.0.7/anyconfig
  creating anyconfig-0.0.7/anyconfig.egg-info
  creating anyconfig-0.0.7/anyconfig/backend
  creating anyconfig-0.0.7/anyconfig/backend/tests
  creating anyconfig-0.0.7/anyconfig/tests
  creating anyconfig-0.0.7/docs
  creating anyconfig-0.0.7/pkg
  making hard links in anyconfig-0.0.7...
  hard linking LICENSE.MIT -> anyconfig-0.0.7
  hard linking MANIFEST.in -> anyconfig-0.0.7
  hard linking README.rst -> anyconfig-0.0.7
  hard linking package.spec.in -> anyconfig-0.0.7
  hard linking setup.py -> anyconfig-0.0.7
  hard linking anyconfig/__init__.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig/api.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig/cli.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig/compat.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig/globals.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig/init.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig/mergeabledict.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig/parser.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig/template.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig/utils.py -> anyconfig-0.0.7/anyconfig
  hard linking anyconfig.egg-info/PKG-INFO -> anyconfig-0.0.7/anyconfig.egg-info
  hard linking anyconfig.egg-info/SOURCES.txt -> anyconfig-0.0.7/anyconfig.egg-info
  hard linking anyconfig.egg-info/dependency_links.txt -> anyconfig-0.0.7/anyconfig.egg-info
  hard linking anyconfig.egg-info/entry_points.txt -> anyconfig-0.0.7/anyconfig.egg-info
  hard linking anyconfig.egg-info/top_level.txt -> anyconfig-0.0.7/anyconfig.egg-info
  hard linking anyconfig/backend/__init__.py -> anyconfig-0.0.7/anyconfig/backend
  hard linking anyconfig/backend/backends.py -> anyconfig-0.0.7/anyconfig/backend
  hard linking anyconfig/backend/base.py -> anyconfig-0.0.7/anyconfig/backend
  hard linking anyconfig/backend/ini_.py -> anyconfig-0.0.7/anyconfig/backend
  hard linking anyconfig/backend/json_.py -> anyconfig-0.0.7/anyconfig/backend
  hard linking anyconfig/backend/xml_.py -> anyconfig-0.0.7/anyconfig/backend
  hard linking anyconfig/backend/yaml_.py -> anyconfig-0.0.7/anyconfig/backend
  hard linking anyconfig/backend/tests/__init__.py -> anyconfig-0.0.7/anyconfig/backend/tests
  hard linking anyconfig/backend/tests/backends.py -> anyconfig-0.0.7/anyconfig/backend/tests
  hard linking anyconfig/backend/tests/base.py -> anyconfig-0.0.7/anyconfig/backend/tests
  hard linking anyconfig/backend/tests/ini_.py -> anyconfig-0.0.7/anyconfig/backend/tests
  hard linking anyconfig/backend/tests/json_.py -> anyconfig-0.0.7/anyconfig/backend/tests
  hard linking anyconfig/backend/tests/nojson.py -> anyconfig-0.0.7/anyconfig/backend/tests
  hard linking anyconfig/backend/tests/noyaml.py -> anyconfig-0.0.7/anyconfig/backend/tests
  hard linking anyconfig/backend/tests/xml_.py -> anyconfig-0.0.7/anyconfig/backend/tests
  hard linking anyconfig/backend/tests/yaml_.py -> anyconfig-0.0.7/anyconfig/backend/tests
  hard linking anyconfig/tests/00.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/__init__.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/api.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/cli.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/common.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/globals.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/init.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/lib.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/mergeabledict.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/parser.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/template.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking anyconfig/tests/utils.py -> anyconfig-0.0.7/anyconfig/tests
  hard linking docs/anyconfig_cli.1 -> anyconfig-0.0.7/docs
  hard linking pkg/entry_points.txt -> anyconfig-0.0.7/pkg
  hard linking pkg/nose.cfg -> anyconfig-0.0.7/pkg
  hard linking pkg/pylintrc -> anyconfig-0.0.7/pkg
  hard linking pkg/rpmbuild-wrapper.sh -> anyconfig-0.0.7/pkg
  hard linking pkg/runtest.sh -> anyconfig-0.0.7/pkg
  hard linking pkg/test_requirements-py-2.6.txt -> anyconfig-0.0.7/pkg
  hard linking pkg/test_requirements.txt -> anyconfig-0.0.7/pkg
  Writing anyconfig-0.0.7/setup.cfg
  Creating tar archive
  removing 'anyconfig-0.0.7' (and everything under it)
  sh: 0 行: fg: ジョブ制御が無効になっています
  書き込み完了: /home/ssato/repos/public/github.com/ssato/python-anyconfig.git/dist/python-anyconfig-0.0.7-1.fc21.src.rpm
  ssato@localhost%               ~/repos/public/github.com/ssato/python-anyconfig.git

無事 Source RPM ができたのでビルド、リリース。

ターゲットは RHEL 7 / Fedora 20, 21 で並列ビルド、リリース
(社内の自分の yum リポジトリへ)。

リリースのためのビルド、リリース処理そのものは
`myrepo <https://github.com/ssato/python-myrepo>` を利用。
(当然 myrepo も同じ仕組みでビルド、リリースしていて yum でインストール可能。)

.. code-block:: console

  ssato@localhost% myrepo d dist/python-anyconfig-0.0.7-1.fc21.src.rpm
  21:47:24 [INFO] myrepo: Run myrepo.commands.deploy.run...
  INFO: mock.py version 1.2.7 starting (python version = 2.7.8)...
  Start: init plugins
  INFO: mock.py version 1.2.7 starting (python version = 2.7.8)...
  INFO: selinux enabled
  INFO: mock.py version 1.2.7 starting (python version = 2.7.8)...
  Start: init plugins
  Start: init plugins
  Finish: init plugins
  Start: run
  INFO: Start(dist/python-anyconfig-0.0.7-1.fc21.src.rpm)  Config(fedora-21-x86_64)
  Start: clean chroot
  INFO: selinux enabled
  INFO: selinux enabled
  Finish: init plugins
  Start: run
  Finish: init plugins
  Start: run
  INFO: Start(dist/python-anyconfig-0.0.7-1.fc21.src.rpm)  Config(fedora-20-x86_64)
  Start: clean chroot
  INFO: Start(dist/python-anyconfig-0.0.7-1.fc21.src.rpm)  Config(rhel-7-x86_64)
  Start: clean chroot
  Finish: clean chroot
  Start: chroot init
  INFO: calling preinit hooks
  INFO: enabled root cache
  Start: unpacking root cache
  Finish: clean chroot
  Finish: clean chroot
  Start: chroot init
  Start: chroot init
  INFO: calling preinit hooks
  INFO: enabled root cache
  Start: unpacking root cache
  INFO: calling preinit hooks
  INFO: enabled root cache
  Start: unpacking root cache
  Finish: unpacking root cache
  INFO: enabled yum cache
  Start: cleaning yum metadata
  Finish: cleaning yum metadata
  INFO: enabled ccache
  Mock Version: 1.2.7
  INFO: Mock Version: 1.2.7
  Start: yum update
  Finish: unpacking root cache
  INFO: enabled yum cache
  Start: cleaning yum metadata
  Finish: unpacking root cache
  INFO: enabled yum cache
  Start: cleaning yum metadata
  Finish: cleaning yum metadata
  INFO: enabled ccache
  Finish: cleaning yum metadata
  INFO: enabled ccache
  Mock Version: 1.2.7
  INFO: Mock Version: 1.2.7
  Mock Version: 1.2.7
  INFO: Mock Version: 1.2.7
  Start: yum update
  Start: yum update
  Finish: yum update
  Finish: chroot init
  Start: build phase for python-anyconfig-0.0.7-1.fc21.src.rpm
  Start: build setup for python-anyconfig-0.0.7-1.fc21.src.rpm
  Finish: build setup for python-anyconfig-0.0.7-1.fc21.src.rpm
  Start: rpmbuild python-anyconfig-0.0.7-1.fc21.src.rpm
  Finish: rpmbuild python-anyconfig-0.0.7-1.fc21.src.rpm
  Finish: build phase for python-anyconfig-0.0.7-1.fc21.src.rpm
  INFO: Done(dist/python-anyconfig-0.0.7-1.fc21.src.rpm) Config(fedora-21-x86_64) 0 minutes 24 seconds
  INFO: Results and/or logs in: /var/lib/mock/fedora-21-x86_64/result
  Finish: run
  Spawning worker 0 with 1 pkgs
  Workers Finished
  Gathering worker results
  created drpm from python-anyconfig-0.0.6-1.fc21.src to python-anyconfig-0.0.7-1.fc21.src: /home/devel/ssato/public_html/yum/fedora/21/sources/./drpms/python-anyconfig-0.0.6-1.fc21_0.0.7-1.fc21.src.drpm in 0.044

  Saving Primary metadata
  Saving file lists metadata
  Saving other metadata
  Saving delta metadata
  Generating sqlite DBs
  Sqlite DBs complete
  Spawning worker 0 with 2 pkgs
  Workers Finished
  Gathering worker results
  created drpm from python3-anyconfig-0.0.6-1.fc21.noarch to python3-anyconfig-0.0.7-1.fc21.noarch: /home/devel/ssato/public_html/yum/fedora/21/x86_64/./drpms/python3-anyconfig-0.0.6-1.fc21_0.0.7-1.fc21.noarch.drpm in 0.088
  created drpm from python-anyconfig-0.0.6-1.fc21.noarch to python-anyconfig-0.0.7-1.fc21.noarch: /home/devel/ssato/public_html/yum/fedora/21/x86_64/./drpms/python-anyconfig-0.0.6-1.fc21_0.0.7-1.fc21.noarch.drpm in 0.044

  Saving Primary metadata
  Saving file lists metadata
  Saving other metadata
  Saving delta metadata
  Generating sqlite DBs
  Sqlite DBs complete
  Finish: yum update
  Finish: chroot init
  Start: build phase for python-anyconfig-0.0.7-1.fc21.src.rpm
  Start: build setup for python-anyconfig-0.0.7-1.fc21.src.rpm
  Finish: build setup for python-anyconfig-0.0.7-1.fc21.src.rpm
  Start: rpmbuild python-anyconfig-0.0.7-1.fc21.src.rpm
  Finish: rpmbuild python-anyconfig-0.0.7-1.fc21.src.rpm
  Finish: build phase for python-anyconfig-0.0.7-1.fc21.src.rpm
  INFO: Done(dist/python-anyconfig-0.0.7-1.fc21.src.rpm) Config(rhel-7-x86_64) 0 minutes 39 seconds
  INFO: Results and/or logs in: /var/lib/mock/rhel-7-x86_64/result
  Finish: run
  Finish: yum update
  Finish: chroot init
  Start: build phase for python-anyconfig-0.0.7-1.fc21.src.rpm
  Start: build setup for python-anyconfig-0.0.7-1.fc21.src.rpm
  Spawning worker 0 with 1 pkgs
  Workers Finished
  Gathering worker results
  created drpm from python-anyconfig-0.0.6-1.el7.src to python-anyconfig-0.0.7-1.el7.src: /home/devel/ssato/public_html/yum/rhel/7/sources/./drpms/python-anyconfig-0.0.6-1.el7_0.0.7-1.el7.src.drpm in 0.020

  Saving Primary metadata
  Saving file lists metadata
  Saving other metadata
  Saving delta metadata
  Generating sqlite DBs
  Sqlite DBs complete
  Spawning worker 0 with 1 pkgs
  Workers Finished
  Gathering worker results
  created drpm from python-anyconfig-0.0.6-1.el7.noarch to python-anyconfig-0.0.7-1.el7.noarch: /home/devel/ssato/public_html/yum/rhel/7/x86_64/./drpms/python-anyconfig-0.0.6-1.el7_0.0.7-1.el7.noarch.drpm in 0.044

  Saving Primary metadata
  Saving file lists metadata
  Saving other metadata
  Saving delta metadata
  Generating sqlite DBs
  Sqlite DBs complete
  Finish: build setup for python-anyconfig-0.0.7-1.fc21.src.rpm
  Start: rpmbuild python-anyconfig-0.0.7-1.fc21.src.rpm
  Finish: rpmbuild python-anyconfig-0.0.7-1.fc21.src.rpm
  Finish: build phase for python-anyconfig-0.0.7-1.fc21.src.rpm
  INFO: Done(dist/python-anyconfig-0.0.7-1.fc21.src.rpm) Config(fedora-20-x86_64) 0 minutes 56 seconds
  INFO: Results and/or logs in: /var/lib/mock/fedora-20-x86_64/result
  Finish: run
  Spawning worker 0 with 1 pkgs
  Workers Finished
  Gathering worker results
  created drpm from python-anyconfig-0.0.6-1.fc20.src to python-anyconfig-0.0.7-1.fc20.src: /home/devel/ssato/public_html/yum/fedora/20/sources/./drpms/python-anyconfig-0.0.6-1.fc20_0.0.7-1.fc20.src.drpm in 0.028

  Saving Primary metadata
  Saving file lists metadata
  Saving other metadata
  Saving delta metadata
  Generating sqlite DBs
  Sqlite DBs complete
  Spawning worker 0 with 2 pkgs
  Workers Finished
  Gathering worker results
  created drpm from python3-anyconfig-0.0.6-1.fc20.noarch to python3-anyconfig-0.0.7-1.fc20.noarch: /home/devel/ssato/public_html/yum/fedora/20/x86_64/./drpms/python3-anyconfig-0.0.6-1.fc20_0.0.7-1.fc20.noarch.drpm in 0.059
  created drpm from python-anyconfig-0.0.6-1.fc20.noarch to python-anyconfig-0.0.7-1.fc20.noarch: /home/devel/ssato/public_html/yum/fedora/20/x86_64/./drpms/python-anyconfig-0.0.6-1.fc20_0.0.7-1.fc20.noarch.drpm in 0.047

  Saving Primary metadata
  Saving file lists metadata
  Saving other metadata
  Saving delta metadata
  Generating sqlite DBs
  Sqlite DBs complete
  Spawning worker 0 with 2 pkgs
  Workers Finished
  Gathering worker results
  created drpm from python3-anyconfig-0.0.6-1.fc20.noarch to python3-anyconfig-0.0.7-1.fc20.noarch: /home/devel/ssato/public_html/yum/fedora/20/i386/./drpms/python3-anyconfig-0.0.6-1.fc20_0.0.7-1.fc20.noarch.drpm in 0.072
  created drpm from python-anyconfig-0.0.6-1.fc20.noarch to python-anyconfig-0.0.7-1.fc20.noarch: /home/devel/ssato/public_html/yum/fedora/20/i386/./drpms/python-anyconfig-0.0.6-1.fc20_0.0.7-1.fc20.noarch.drpm in 0.045

  Saving Primary metadata
  Saving file lists metadata
  Saving other metadata
  Saving delta metadata
  Generating sqlite DBs
  Sqlite DBs complete
  ssato@localhost%                ~/repos/public/github.com/ssato/python-anyconfig.git

リリース完了したのでこの作業環境そのもの (Fedora 21 Latest) で更新を適用:

.. code-block:: console

  ssato@localhost% grep fedora-nrt-ssato /etc/yum.repos.d/*
  /etc/yum.repos.d/fedora-nrt-ssato.repo:[fedora-nrt-ssato]
  /etc/yum.repos.d/fedora-nrt-ssato.repo:[fedora-nrt-ssato-source]
  ssato@localhost% rpm -qf /etc/yum.repos.d/fedora-nrt-ssato.repo
  fedora-nrt-ssato-release-0.0.4-1.fc21.noarch
  ssato@localhost% sudo dnf clean all && sudo dnf update -y '*anyconfig*'
  Cleaning repos: updates bluejeans adobe-linux-x86_64 rpmfusion-free
                : fedora rpmfusion-free-updates fedora-nrt-ssato
  Cleaning up Everything
  Fedora 21 - x86_64 - Updates                         3.5 MB/s |  20 MB     00:05
  Blue Jeans Network, Inc. - x86_64 software and updat  19 kB/s |  17 kB     00:00
  Adobe Systems Incorporated                           2.4 kB/s | 1.8 kB     00:00
  RPM Fusion for Fedora 21 - Free                       67 kB/s | 522 kB     00:07
  Fedora 21 - x86_64                                   3.6 MB/s |  39 MB     00:10
  RPM Fusion for Fedora 21 - Free - Updates             72 kB/s | 257 kB     00:03
  Custom yum repository on xxxxxxx.redhat.com by ssato  26 kB/s |  55 kB     00:02
  Using metadata from Thu Apr 23 21:49:40 2015
  Dependencies resolved.
  =====================================================================================
   Package                Arch        Version              Repository             Size
  =====================================================================================
  Upgrading:
   python-anyconfig       noarch      0.0.7-1.fc21         fedora-nrt-ssato       86 k
   python3-anyconfig      noarch      0.0.7-1.fc21         fedora-nrt-ssato       87 k

  Transaction Summary
  =====================================================================================
  Upgrade  2 Packages

  Total download size: 173 k
  Downloading Packages:
  (1/2): python3-anyconfig-0.0.6-1.fc21_0.0.7-1.fc21.n  26 kB/s |  36 kB     00:01
  (2/2): python-anyconfig-0.0.7-1.fc21.noarch.rpm       60 kB/s |  86 kB     00:01
  [DRPM] python3-anyconfig-0.0.6-1.fc21_0.0.7-1.fc21.noarch.drpm: done
  -------------------------------------------------------------------------------------
  Total                                                 81 kB/s | 122 kB     00:01
  Delta RPMs reduced 0.2 MB of updates to 0.1 MB (29.1% saved)
  Running transaction check
  Transaction check succeeded.
  Running transaction test
  Transaction test succeeded.
  Running transaction
    Upgrading   : python3-anyconfig-0.0.7-1.fc21.noarch                            1/4
    Upgrading   : python-anyconfig-0.0.7-1.fc21.noarch                             2/4
    Cleanup     : python3-anyconfig-0.0.6-1.fc21.noarch                            3/4
    Cleanup     : python-anyconfig-0.0.6.20150407-1.fc21.noarch                    4/4
    Verifying   : python-anyconfig-0.0.7-1.fc21.noarch                             1/4
    Verifying   : python3-anyconfig-0.0.7-1.fc21.noarch                            2/4
    Verifying   : python3-anyconfig-0.0.6-1.fc21.noarch                            3/4
    Verifying   : python-anyconfig-0.0.6.20150407-1.fc21.noarch                    4/4

  Upgraded:
    python-anyconfig.noarch 0.0.7-1.fc21     python3-anyconfig.noarch 0.0.7-1.fc21

  Complete!
  ssato@localhost%

.. vim:sw=2:ts=2:et:
