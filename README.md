# Irab-scraper
This effort will look to take data from the al-I’rāb al-Mufassal (by Bahjat Abdul Wahid Saleh) and structure it for data analysis


# Flask API Doc
you need to have `docker` installed

just run the start.sh file in sudo mode
```sudo sh start.sh```

the container will start

## Examples
### use this command for interaction
```
❯ curl -X GET -H "Content-type: application/json" -d "{\"surah\" : \"10\", \"ayah\" : \"82\", \"word\" : \"1\"}" "localhost:56733/irreb"

{"irrab":" الواو استئنافية. يحق: فعل مضارع مرفوع بالضمة. الله لفظ الجلالة: فاعل مرفوع للتعظيم بالضمة."}
```

```
❯ curl -X GET -H "Content-type: application/json" -d "{\"surah\" : \"10\", \"ayah\" : \"82\", \"word\" : \"3\"}" "localhost:56733/irreb"

{"irrab":" الحق: مفعول به منصوب بالفتحة - أي يبينه. بكلماته: جار ومجرور متعلق بيحق والهاء ضمير متصل مبني على الكسر في محل جر بالإضافة.\n"}
```