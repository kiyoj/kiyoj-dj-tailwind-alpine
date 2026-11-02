# pip install django-tailwind
### tailwind start
python manage.py tailwind start
これにより
/themeに設定ファイルが作られる
/theme/static/css/dist/style.css
このファイルは makedownに影響を受けるようだ
以下のように変更した
## h1 - h6
h1 {
  font-size: 2.25rem;
	font-weight: 700;
}
h2 {
  font-size: 1.875rem;
	font-weight: 700;
}
h3 {
  font-size: 1.5rem;
	font-weight: 700;
}
h4 {
  font-size: 1.25rem;
	font-weight: 700;
}
h5 {
  font-size: 1.125rem;
	font-weight: 700;
}
h6 {
  font-size: 1rem;
  font-weight: 700;
}

# a - a:hover
a {
  color: #4299e1;
	text-decoration: none;
}

a:hover {
	color: #3182ce;
	text-decoration: underline;
}
# code , pre
/*
code,
kbd,
samp,
*/
code,
pre {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  /* 1 */
  font-feature-settings: normal;
  /* 2 */
  font-variation-settings: normal;
  /* 3 */
  font-size: 1em;
  /* 4 */
  border-radius: 10px;
}
### Create superuser

user: kiyo
email: kiyo@yosiki.org
password: 

# jsonデータをエクスポート
python manage.py dumpdata > data.json
# jsonデータからインポート
python manage.py loaddata data.json

旧象歩 http://owa.as.wakwak.ne.jp