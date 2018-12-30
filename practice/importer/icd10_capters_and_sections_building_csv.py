import xml.parsers.expat
import csv


path, value, codes = [], [], []
chapter_name = chapter_description = section_name = section_description = code_name = code_description = None


def path_ends_in(value: str):
    value = value.split('/')
    if len(path) >= len(value):
        if path[-len(value):] == value[-len(value):]:
            return True
    return False


# 3 handler functions
def start_element(name, attrs):
    global section_name
    value.clear()
    path.append(name)

    if path_ends_in('chapter/sectionIndex/sectionRef'):
        section_name = attrs.get('id')
    elif path_ends_in('diag'):
        if len(codes) > 0 and codes[-1][-1] != 'category_code':
            codes[-1].append('category_code')
        codes.append([])


def char_data(data):
    value.append(data)


def end_element(name):
    global chapter_name, chapter_description, section_description, code_name, code_description
    if path_ends_in('chapter/desc'):
        chapter_description = ''.join(value).strip()
    elif path_ends_in('chapter/name'):
        chapter_name = ''.join(value).strip()
    elif path_ends_in('chapter/sectionIndex/sectionRef'):
        section_description = ''.join(value).strip()
        sections_writer.writerow([section_name, section_description, chapter_name])
    elif path_ends_in('diag/name'):
        codes[-1].append(''.join(value).strip())
    elif path_ends_in('diag/desc'):
        codes[-1].append(''.join(value).strip())
    elif path_ends_in('chapter'):
        chapters_writer.writerow([chapter_name, chapter_description])
    elif path_ends_in('diag'):
        code = codes[-1][0]
        description = codes[-1][1]
        billalbe = not (len(codes[-1]) > 2 and codes[-1][2] == 'category_code')
        icd10_writer.writerow([code, description, billalbe, section_name, section_description, chapter_name, chapter_description])
        del codes[-1]

    del path[-1]
    value.clear()


p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data
csv.register_dialect('custom_dialect', delimiter=';', quoting=csv.QUOTE_NONE)

with open('chapters.csv', 'w') as chapters_file, open('sections.csv', 'w') as sections_file, \
        open('icd10.csv', 'w') as icd10_file:

    chapters_fieldnames = ['title', 'description']
    chapters_writer = csv.writer(chapters_file, dialect='custom_dialect')
    chapters_writer.writerow(chapters_fieldnames)

    sections_fieldnames = ['title', 'description', 'chapterTitle']
    sections_writer = csv.writer(sections_file, dialect='custom_dialect')
    sections_writer.writerow(sections_fieldnames)

    icd10_fieldnames = ['code', 'description', 'billable', 'sectionTitle', 'sectionDescription', 'chapterTitle', 'chapterDescription']
    icd10_writer = csv.writer(icd10_file, dialect='custom_dialect')
    icd10_writer.writerow(icd10_fieldnames)

    p.ParseFile(open('icd10cm_tabular_2018.xml', 'rb'))
