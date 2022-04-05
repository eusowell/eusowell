from jinja2 import Environment, FileSystemLoader
import os
import json



def gera_html(user):
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('index.html')

    with open('data.json', 'r') as fp:
        data = json.load(fp)

    sem_tel = []

    for d in data:
        # print(d['phones'][0])
        if user in d['primaryEmail']:
            print(f'Usuário: {d["name"]["fullName"]}')
            if '/Administradores' == d['orgUnitPath']:
                unidade = 'Minas Gerais'
            else:
                characters = "/"
                unidade = d['orgUnitPath']
                unidade = ''.join(x for x in unidade if x not in characters)

            mobile = ''
            work = ''

            if 'phones' in d:
                # print(len(d['phones']))
                for n in range(len(d['phones'])):
                    if 'mobile' in d['phones'][n]['type']:
                        mobile = d['phones'][n]['value']
                    if 'work' in d['phones'][n]['type']:
                        work = d['phones'][n]['value']
            else:
                print('sem telefone')
                sem_tel.append(d["name"]["fullName"])

            filename = os.path.join(root, 'html', f'{d["name"]["fullName"]}.html')
            with open(filename, 'w') as fh:
                fh.write(template.render(
                    FirstName=d['name']['givenName'],
                    LastName=d['name']['familyName'],
                    CompanyName='Pinto & Soares Advogados Associados',
                    PhoneWork=work,
                    PhoneMobile=mobile,
                    Email=d['primaryEmail'],
                    OrgUnitPath=unidade,
                ))
            return filename
