import json
d ={
    "name":"V",
    "age":28,
    "gender":"male"
}
#ensure_ascii=False使中文能正常显示
s = json.dumps(d,ensure_ascii=False)
print(s)

l = [
    {
        "name":"V",
        "age":28,
        "gender":"male"
    },
    {
        "name": "亨利",
        "age": 20,
        "gender": "male"
    },
    {
        "name": "阿米娅",
        "age": 19,
        "gender": "female"
    },
]

print(json.dumps(l,ensure_ascii=False))
json_str = '{"name": "V", "age": 28, "gender": "male"}'
json_array_str = '[{"name": "V", "age": 28, "gender": "male"}, {"name": "亨利", "age": 20, "gender": "male"}, {"name": "阿米娅", "age": 19, "gender": "female"}]'

#类型自动转换
res_dict = json.loads(json_str)
print(res_dict,type(res_dict))

res_list = json.loads(json_array_str)
print(res_list,type(res_list))