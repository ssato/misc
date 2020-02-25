(この記事は https://qiita.com/advent-calendar/2019/ansible2 の 12/16 分の投稿となります。)

# 概要

本記事では Assertive Programming (表明プログラミング) が堅牢な Ansible Playbook・Role を実装するための一助となることを、いくつかの例もあげて簡単に説明します。

# Ansible における変数の諸問題

Ansible Playbook・Role 一般に対象や環境の差異などに柔軟に対応して共通化したり、またある程度の拡張性を持たせようとしたりしようとするとほぼ必ず *変数* (*variable*) を使うことになるでしょう。また一切変数を使わず Ansible Playbook・Role を書くと、非常に硬直した、特定の対象、環境、設定などにしか対応できないものとなってしまいます。故に Ansible Playbook・Role を書く際に変数がまったく登場しないということはごくまれでしょうし、変数の扱いは非常に重要であるといえます。

しかし残念ながら Ansible 世界での *変数* は他のプログラミング言語における *変数* またはそれに類するものと比較すると非常に貧弱に感じます。これは最終的に Ansible Playbook が Python スクリプトに変換されるからということもあるのですが、例えば Ansible での変数には、最近のモダンなプログラミング言語では当たり前のように備わっている機能や性質がなく、堅牢な Ansible Playbook・Role の開発を妨げることになる次のような問題があるように思います。

- グローバル変数のみ
- Namespace 的なものはない
- どこでも宣言でき、後でいつでも上書き/変更されうる
- 未定義でも警告はされず実行時にエラーともならない
- 値が空でも警告はされず実行時にエラーとはならない
- 変数の (暗黙に前提とされていた) 型と実際に指定された値の型が不一致でも基本的には警告等はなされず、実行時にエラーとはならない
- bool 型や string 型への暗黙のキャストがあり、無効化できない
- etc

こういった問題をすべて解決できるわけではないですが、この中のいくつかは『運用でカバー』、つまり Ansible Playbook・Role 開発を行う側の少しの追加の努力によって、改善をはかることができそうです。

この記事ではその一つ、Assertive Programming (表明プログラミング) による改善案の具体例をいくつか示し、それぞれの効果について簡単に説明します。

# Assertive Programming (表明プロラグミング)

Assertive Programming による Ansible Playbook・Role の改善についてふれる前にそもそも Assertive Programming とは何かを簡単に説明します。

Assertion や表明プログラミング、assertive programming といった語句で検索するといくつか説明がみつかります。

- [Packages for Assertive Programming - CRAN][1]
- [Assertion (software development) - Wikipedia][2]
- [表明 (Assertion) - Wikipedia][3]

それぞれ多少の違いはあれどおおまかには次のようなものが Assertive Programming であるといえそうです。

- Fail first (失敗するなら早めに) を目的の一つとする Defensive Programming  (防衛的または防御的プログラミング) の手法の一つ
- 何か処理を行う前に、当然そうなっているべきと期待される事前条件が期待どおり満足されていることを表明する (assert) コードを書く

  - 例 0. ある変数が宣言済みであることを表明
  - 例 1. ある変数が宣言済みで null (何らかの未定義の値を示すもの) ではなく、何か意味のある値が設定されていることを表明
  - 例 2. 関数の冒頭で変数の型が期待どおりであることを表明
  - 例 3. 関数の冒頭で変数の値が期待どおりの値域にあることを表明

- 表明したとおりになっていなかったら即座にプログラムは停止し、その先の処理は実行されない

  - 例. python では厳密には AssertionError 例外が raise される

Assertive Programming により特殊で異常な状況 (期待される事前条件が満足されていない) をとらえ、それ以上は処理を勝手に進めてよりまずい状況を防ぐことができる、より堅牢なコードとなることが期待できます。

より具体的な Assertive Programming のイメージをつかみやすいように、まったく実際的ではないかもしれませんしやや無理矢理感もありますが、python でのコード例をいくつか示します。

```python
# 例 0. グローバル変数 FOO は定義済みのはず (globals(): 定義済みのグローバル変数名をキーに、変数の値を値とする辞書を返す関数)
assert 'FOO' in globals()

# 例 1. FOO は None (None は python での NULL / Nothing 的なもの、singleton なので is not で None ではないことを確認できる)
assert FOO is not None

def do_something(foo=FOO):
    assert isinstance(foo, int)  # 例 2. foo は int (整数型の一種) のはず
    assert 0 < foo < 4           # 例 3. foo の値は 1, 2, 3 のいずれか
    return _do_something(foo)    # (1, 2, 3) のどれかの値に限り可能な何らかの処理を実行し返す ...
```

なお厳密には表明 (assertion) は真に異常な場合のみを扱うことが多くて、例えば値の確認などは表明ではなく if 文など条件分岐してで陽に確認、問題に対処する方がより一般的かもしれません。しかし話を簡単にするために、以降では意図的に表明 (assertion) の適用範囲を広げ、通常他のプログラミング言語では
表明を使わず記述するようなものも対象とします。

## Assertion がないとまずい例

ここまで変数そのものやその値を色々確認してないとまずいのでは? という前提で説明していますが非常にまずいことが起りそうな例を一つだけあげておきます。

```yaml
# 絶対実行してはいけない Ansible Playbook
- hosts: localhost
  gather_facts: false
  connection: local
  become: true
  var:
    workdir: ""  # Danger!
  tasks:
    # Disaster!!
    - name: Balse!
      command: >-
       rm -rf /{{ workdir }}
```

*間違っても上記 Playbook を sudo NOPASSWORD 可能なユーザーで実行などは絶対しないように!!!*

# Assertive Programming in Ansible

Ansible にも assert モジュールなるものがあり、これを使えば Assertive Programming を実現できそうですので試してみます。

## 変数定義の確認

assert モジュールの使い方ですが、簡単には次のような感じで書けます。(詳細は ansible-doc assert の説明をご覧下さい。)

```yaml
- name: <assert task の description ...>
  assert:
    that:
      - 表明その一 (真偽値に評価されるような式を書く)
      - 表明その二
        ... # 以降中略、後略を '...' で表記します
    fail_msg: <順番に表明を評価してどれか false になったら即座に処理を止め、出力されるメッセージ>
```

- that 節に最終的に評価された結果 true/false になるような Jinja2 テンプレートの式を列挙
- fail_msg 節に文字列を指定しておくと assertion が失敗したときに出力してくれる

実際に assert モジュールを使って python コードでやったように変数が定義されているかどうか確認してみましょう。少々長いですが定義済みかどうかは [defined という Jinja 2 の Builtin test][4] で可能です。

- [変数が定義済みかどうか確認する例][5] の抜粋

  ```yaml
  - name: Check variables may have primitive values are defined
    assert:
      that:
        - sape_do_more_advanced_checks is defined
          ...
  ```

- [上記で参照している変数の default 定義][6]

## 変数の型チェック

同様に assert モジュールを使って python コードでやったように変数の型チェックを行ってみましょう。

- [変数の型チェック例][9]

  ```yaml
  - name: Check the types of the variables may have primitive values
    assert:
      that:
        - sape_a_str_0 is string
          ...
      fail_msg: |
        - sape_a_str_0: {{ sape_a_str_0 | d() }}
          ...

  - name: Check the types of the variables may have non primitive values
    assert:
      that:
        - sape_a_list_0 is sequence
          ...
      fail_msg: |
        - sape_a_list_0: {{ sape_a_list_0 | d() | to_nice_json }}
          ...
  ```

実際型チェックに使える型を確認する Jinja 2 の test は非常に限られていて、例えば正確に string の要素で構成される list であるかどうかといった型チェックはできないのですが、文字列と数の違いなどは確認できます。

なお変数が定義済みかどうかなどによらず debug 目的で fail_msg 等に出力したい場合、この例のように d filter ([Jinja2 の default filter][7] の alias) などを使うと良いでしょう。そしてそのとき変数が list や mapping 型となりうる可能性のある場合はそのままでは出力できないので、文字列として表現されるように [Ansible Jinja 2 拡張の to_nice_json filter][8] などもあわせて使うと良いでしょう。

## 変数の値チェック

今度は assert モジュールを使って先の python のコード例のように変数の値チェックを行ってみましょう。

- [変数の値チェック例][10] の抜粋

```yaml

- name: Check values of the variables should have primitive values
  assert:
    that:
      - sape_do_more_advanced_checks in [true, false]
        ...
      - sape_a_str_1 | length > 0
      - sape_a_int_0 == 0
      - sape_a_int_1 != 0
      - sape_a_int_1 > 0
        ...

- name: Check values of the variables may have non primitive values
  assert:
    that:
      ...
      - sape_a_dict_1 | length > 0
      - sape_a_dict_1.a != 0
      - sape_a_dict_1.a > 0
      - sape_a_dict_1.b | length > 0
        ...
```

型チェックでは無理なもの、例えば boolean 型のチェックなども値チェックで代替できる場合があります。またどうやら値を持つ list や dict を bool でキャストしても python とは違い true とはならないようです。この制約は少し残念ですが lengh > 0 等で代替しておきます。

## 他のより複雑な "表明" によるチェックなど

assert モジュールだけでなく、表明とはもはや呼べませんが広義の事前条件のチェックということで command モジュールなど他の方法で確認するタスクを Fail First を優先して含めてしまっても良いでしょう。

- [他のより複雑な "表明" によるチェックの例][11]

command モジュールなど、失敗すると即座にエラーとなるものはそのまま、そうではないものは assert も組み合わると良いでしょう。

# まとめ

- Ansible では変数の制約や機能が弱く、コードの堅牢性に影響
- Ansible でも assert モジュールなどを使えば Assertive Programming できる
- Ansible でも Assertive Programming すれば Fail First しつつ Defensive Programming できる

<!-- links:
-->
[1]: https://cran.r-project.org/web/packages/checkr/vignettes/assertive-programming.html
[2]: https://en.wikipedia.org/wiki/Assertion_(software_development)
[3]: https://ja.wikipedia.org/wiki/%E8%A1%A8%E6%98%8E
[4]: https://jinja.palletsprojects.com/en/2.10.x/templates/#defined
[5]: https://github.com/ssato/ansible-role-assertive-programming-examples/blob/master/tasks/pre_def_checks.yml
[6]: https://github.com/ssato/ansible-role-assertive-programming-examples/blob/master/defaults/main.yml
[7]: https://jinja.palletsprojects.com/en/2.10.x/templates/#default
[8]: https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#filters-for-formatting-data
[9]: https://github.com/ssato/ansible-role-assertive-programming-examples/blob/master/tasks/pre_type_checks.yml
[10]: https://github.com/ssato/ansible-role-assertive-programming-examples/blob/master/tasks/pre_value_checks.yml
[11]: https://github.com/ssato/ansible-role-assertive-programming-examples/blob/master/tasks/pre_more_advanced_checks.yml

<!-- vim:sw=2:ts=2:et:
-->
