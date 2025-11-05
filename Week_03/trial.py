from jinja2 import Template

template = Template("""
my name is {{var}}
""")

template2 = Template("""
{% for i in collection %}
            {{i}}
{% endfor %}
""")

output1 = template.render(var="Roshni")
output2 = template2.render(collection=[1,2,3])

print(output1)
print(output2)