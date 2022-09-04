# uml-to-code projet
# ==================
# Bundle version 1.0
# ==================

from xml.dom import minidom
from unidecode import unidecode

"""
mapping
"""
def attributesepararor(val):
    info={}
    visibility=["-","*",'~',"+","#"]
    if val[0] in visibility:
        info["visibility"]=val[0]
        val=val.replace(val[0],"")

    if ":" in val:
        tmp=val.split(":")
        info["nom"]=tmp[0]

        if "=" in tmp[1]:
            tmp2=tmp[1].split("=")
            info["type"]=tmp2[0]
            info["default"]=tmp2[1]
        else:
            info["type"]=tmp[1]
    else:
        info["nom"]=val



    return info

def operateurseperate(val):
    info = {}
    visibility = ["-", "*", '~', "+", "#"]
    if val[0] in visibility:
        info["visibility"] = val[0]
        val = val.replace(val[0], "")
    tmp=val.split("(")
    info["nom"]=tmp[0]

    if ":" in tmp[1]:

        tmp2=tmp[1].split(":")
        info["variable"]=tmp2[0].replace(")","")
        info["retour"]=tmp2[1]
    else:
        info["variable"] = tmp[1].replace(")", "")

    return info

"""
code structure
"""
#Python
CODE="""
class {name}:
    def __init__(self,{attributs}):
        {attr_in_const}

{opr_in_const}
    """

OPR="""
    def {nom}(self,{variable}):
        pass
    """

#JAVA
CODE_JAVA="""

class {name}{sepd}
    //Les attributs
    {attributs}
    
    //Les constructeurs
    {name}({variables}){sepd}
        {var_in_const}
    {sepf}
    
        {opr_in_const}
    {sepf}
"""

OPR_JAVA="""
 void {nom}({variables}){sepd}
      pass
   {sepf}    
"""

"""
java_code_generator
"""
def mapping_operation_java(op):
    """
    fonction callback de Mapping de la liste opération en string spécial
    :param op:
    :return:
    """
    #var=unidecode(",".join(list(map(lambda x:f"{x.get('type')} {x.get('nom')}",op.get("variable")))))
    #vars="" if len(op.get('variable'))==0 else var
    return OPR_JAVA.format(nom=op.get("nom","undifined"),variables=op.get('variable'),sepf="}",sepd='{')

def generator_in_java(dico):
    """
    Générer a partir d'un dictionaire de la forme {'undefined:UMLClass_6': {'name': 'collège', 'attribut': ['code_collège', 'nom', 'adresse_site'], 'operations': []} le code de la classe
    :param dico:
    :return:String unique de la classe
    """
    attributs=unidecode("\n\t".join(list(map(lambda x:f"private {x.get('type')} {x['nom']};",dico["attribut"]))))
    variables=unidecode(",".join(list(map(lambda x:f"{x.get('type')} {x['nom']}",dico["attribut"]))))
    var_in_const="\n\t\t".join(list(map(lambda x:f"this.{unidecode(x['nom'])}={unidecode(x.get('nom','undifined'))};",dico["attribut"])))
    opr_in_const="\n\t".join(list(map(mapping_operation_java,dico["operations"])))
    return CODE_JAVA.format(name=unidecode(dico["name"]).capitalize(),variables=variables,sepd='{',sepf='}',attributs=attributs,var_in_const=var_in_const,opr_in_const=opr_in_const)

def code_generator_java_full(classes):
    """
    Générer en prenant la liste de tous les classes du systeme tout le code de base
    :param classes:
    :return:
    """

    return "".join(list(map(lambda clr:generator_in_java(clr),classes.values())))

"""
python_code_generator
"""
def mapping_operation(op):
    """
    fonction callback de Mapping de la liste opération en string spécial
    :param op:
    :return:
    """
    return OPR.format(nom=op.get("nom","undifined"),variable=op.get("variable",""))

def generator_in_python(dico):
    """
    Générer a partir d'un dictionaire de la forme {'undefined:UMLClass_6': {'name': 'collège', 'attribut': ['code_collège', 'nom', 'adresse_site'], 'operations': []} le code de la classe
    :param dico:
    :return:String unique de la classe
    """

    #Les attributs
    attr=unidecode(",".join(list(map(lambda x:f"{x['nom']}",dico["attribut"]))))
    #Attributs dans constructeur
    attr_in_const="\n        ".join(list(map(lambda x:f"self.{unidecode(x['nom'])}={unidecode(x.get('nom','undifined'))}",dico["attribut"])))

    #Operation
    opr_in_const="\n\t".join(list(map(mapping_operation,dico["operations"])))

    return CODE.format(name=unidecode(dico["name"]).capitalize(), attributs=attr, attr_in_const=attr_in_const,opr_in_const=opr_in_const)

def code_generator_python_full(classes):
    """
    Générer en prenant la liste de tous les classes du systeme tout le code de base
    :param classes:
    :return:
    """
    return "".join(list(map(lambda clr:generator_in_python(clr),classes.values())))


"""
xmlReader
"""
def read_file_xml(chemin, use_string:bool=False):
    summary={}
    temp={}
    classes={}
    gens={}
    ass={}
    comps={}
    aggs={}

    dom=""
    if not use_string:
        with open(chemin,"r") as f:
            dom=minidom.parse(f, parser=None, bufsize=None)
    else:
        dom=minidom.parseString(chemin)

    principal=dom.getElementsByTagName("UMLClassDiagram")[0]
    #print(principal.toxml())
    nameglobal=principal.getAttribute("name")

    for classe in principal.getElementsByTagName("UMLClass"):
        tmp={}
        tmp["name"]=[item.getAttribute("value") for item in classe.getElementsByTagName("item")][0]


        for super_item in classe.getElementsByTagName("superitem"):
            if super_item.getAttribute("id")=="attributes":
                attribut=[attr.getAttribute("value") for attr in super_item.getElementsByTagName('item')]
            elif super_item.getAttribute("id")=="operations":
                operations=[attr.getAttribute("value") for attr in super_item.getElementsByTagName('item')]
                tmp["attribut"] = list(map(attributesepararor, attribut))
                nb=len([x.get('type') for x in tmp["attribut"] if x.get("type")!=None])
                tmp["is_typed"]=len(tmp["attribut"])==nb
                # print(len(tmp["attribut"]),nb)
                # print([x.get('type') for x in tmp["attribut"]])


        tmp["operations"]=list(map(operateurseperate,operations))
        classes[classe.getAttribute("id")]=tmp



    for gen in principal.getElementsByTagName("UMLGeneralization"):
        tmp={}

        tmp["side_A"]=gen.getAttribute("side_A")
        tmp["side_B"]=gen.getAttribute("side_B")
        tmp["direction"]=gen.getAttribute("direction")
        for items in gen.getElementsByTagName("item"):
            if items.getAttribute("id") == "name":
                tmp["name"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "roleA":
                tmp["role_A"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "roleB":
                tmp["role_B"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "multiplicityA":
                tmp["multiA"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "multiplicityB":
                tmp["multiB"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]

        gens[gen.getAttribute("id")]=tmp

    for gen in principal.getElementsByTagName("UMLAssociation"):
        tmp = {}

        tmp["side_A"] = gen.getAttribute("side_A")
        tmp["side_B"] = gen.getAttribute("side_B")
        tmp["direction"] = gen.getAttribute("direction")
        for items in gen.getElementsByTagName("item"):
            if items.getAttribute("id") == "name":
                tmp["name"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "roleA":
                tmp["role_A"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "roleB":
                tmp["role_B"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "multiplicityA":
                tmp["multiA"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "multiplicityB":
                tmp["multiB"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]

        ass[gen.getAttribute("id")] = tmp

    for gen in principal.getElementsByTagName("UMLComposition"):
        tmp = {}

        tmp["side_A"] = gen.getAttribute("side_A")
        tmp["side_B"] = gen.getAttribute("side_B")
        tmp["direction"] = gen.getAttribute("direction")
        for items in gen.getElementsByTagName("item"):
            if items.getAttribute("id") == "name":
                tmp["name"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "roleA":
                tmp["role_A"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "roleB":
                tmp["role_B"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "multiplicityA":
                tmp["multiA"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "multiplicityB":
                tmp["multiB"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]

        comps[gen.getAttribute("id")] = tmp

    for gen in principal.getElementsByTagName("UMLAggregation"):
        tmp = {}

        tmp["side_A"] = gen.getAttribute("side_A")
        tmp["side_B"] = gen.getAttribute("side_B")
        tmp["direction"] = gen.getAttribute("direction")
        for items in gen.getElementsByTagName("item"):
            if items.getAttribute("id") == "name":
                tmp["name"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "roleA":
                tmp["role_A"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "roleB":
                tmp["role_B"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "multiplicityA":
                tmp["multiA"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]
            elif items.getAttribute("id") == "multiplicityB":
                tmp["multiB"] = [attr.getAttribute("value") for attr in items.getElementsByTagName('item')]

        aggs[gen.getAttribute("id")] = tmp


    temp["classes"]=classes


    temp["assoc"]=ass


    temp["aggs"]=aggs


    temp["comps"]=comps


    temp["gener"]=gens

    #Final
    summary[nameglobal]=temp

    return summary


"""
main
"""
def to_java(xml:str) -> str:
    r=read_file_xml(xml, use_string=True)
    return code_generator_java_full(r["umldesigner.app"]["classes"])

def to_python(xml:str) -> str:
    r=read_file_xml(xml, use_string=True)
    return code_generator_python_full(r["umldesigner.app"]["classes"])