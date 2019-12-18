import os
import shutil
from src.utils.initCase import initCase


def write_case(_path):
    yml_list = os.listdir(_path)
    project_path = str(os.path.abspath('.').split('src')[0])
    test_path = project_path + '/src/testcase/'
    src = test_path + 'Template.py'
    for case in yml_list:


        if case != '__pycache__':
            data = initCase(case)
            module = data['test_moudle']
            clist = data['test_info']

            yml_name = str(case.split('.')[0])
            case_name = 'test_' + str(yml_name) + '.py'
            new_case = os.path.join(test_path,case_name)
            # if case_name in os.listdir(test_path):
            #     pass
            # else:
            shutil.copyfile(src, new_case)
            with open(new_case, 'r') as fw:
                source = fw.readlines()
            n = 0
            with open(new_case, 'w') as f:
                for line in source:
                    if 'CaseData = initCase' in line:
                        line = line.replace("Template.yml", case)
                        f.write(line)
                        n = n + 1
                    elif 'Moudle' in line:
                        line = line.replace('Moudle', module)
                        f.write(line)
                        n = n + 1
                    elif 'S' in line:
                        for j in range(len(clist)):
                            for i in range(n, len(source)):
                                if 'S' in source[i]:
                                    f.write(source[i].replace("S", clist[j]['dec']))
                                elif 'testCase' in source[i]:
                                    f.write(source[i].replace("testCase", "testCase_0%d" % (j + 1)))
                                elif 'admin' in source[i]:
                                    f.write(source[i].replace("admin", clist[j]['dec']))
                                elif '[0]' in source[i]:
                                    f.write(source[i].replace("[0]", "[%d]" % (j)))
                                else:
                                    f.write(source[i])
                        break
                    else:
                        f.write(line)
                        n += 1
        else:
            continue


if __name__ == '__main__':
    ym_path = '/Users/wanghaitao/Downloads/web_template_pytest/src/field'
    write_case(ym_path)

