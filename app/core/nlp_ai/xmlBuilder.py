from enum import Enum
from xml.dom import minidom

# Constant
BACKGROUND_COLOR = "#ffffbb"
LINE_COLOR = "#294253"
LINE_WIDTH = "1"
ABSTRACT = "false"
PIXEL_LETTER = 10
BOX_PADDING = 30


def xmlGenerator(type: Enum, data: dict):
    # Create xml root for appropriate type of diagram.
    root = minidom.Document()
    xml = root.createElement(type.name)
    xml.setAttribute('name', type.value)

    # Set tables structure for main xml parent.
    for umlTableData in data['allNodes']:
        table = root.createElement(diagramElementTag(type.name))
        table.setAttribute('id', umlTableData['name'])
        table.setAttribute('x', str(umlTableData['x']))
        table.setAttribute('y', str(umlTableData['y']))
        table.setAttribute('width', str(umlTableData['width']))
        table.setAttribute('height', str(umlTableData['height']))
        table.setAttribute('backgroundColor', BACKGROUND_COLOR)
        table.setAttribute('lineColor', LINE_COLOR)
        table.setAttribute('lineWidth', LINE_WIDTH)
        table.setAttribute('tagValues', "")
        table.setAttribute('abstract', ABSTRACT)
        if type.value == "Class diagram":
            item1 = root.createElement("item")
            item1.setAttribute('id', 'name')
            item1.setAttribute('value', umlTableData['name'])
            table.appendChild(item1)

            superItem2 = root.createElement("superitem")
            superItem2.setAttribute('id', 'attributes')
            superItem2.setAttribute('visibleSubComponents', 'true')
            for attribute in umlTableData['attributes']:
                item = root.createElement("item")
                item.setAttribute('value', attribute)
                superItem2.appendChild(item)
            table.appendChild(superItem2)

            superItem3 = root.createElement("superitem")
            superItem3.setAttribute('id', 'operations')
            superItem3.setAttribute('visibleSubComponents', 'true')
            for methods in umlTableData['methods']:
                item = root.createElement("item")
                item.setAttribute('value', methods + "()")
                superItem3.appendChild(item)
            table.appendChild(superItem3)
        xml.appendChild(table)

    # Set relation for diagram
    for relationData in data['relation']:
        if (relationData['type'] == relationType.ASSOCIATION.name) or (relationData['type'] == relationType.RASSOCIATION.name):
            relation = root.createElement(relationType.ASSOCIATION.value)
            relation.setAttribute('id', relationData['t1'] + relationData['t2'])
            relation.setAttribute('side_A', relationData['t1'])
            relation.setAttribute('side_B', relationData['t2'])
            relation.setAttribute('direction', relationData['direction'])
            # Relation item
            item1 = root.createElement("item")
            item1.setAttribute('id', 'name')
            item1.setAttribute('value', relationData['label'])
            relation.appendChild(item1)
            item2 = root.createElement("item")
            item2.setAttribute('id', 'multiplicityA')
            item2.setAttribute('value', relationData['c1'])
            relation.appendChild(item2)
            item3 = root.createElement("item")
            item3.setAttribute('id', 'multiplicityB')
            item3.setAttribute('value', relationData['c2'])
            relation.appendChild(item3)
            item4 = root.createElement("item")
            item4.setAttribute('id', 'roleA')
            item4.setAttribute('value', '')
            relation.appendChild(item4)
            item5 = root.createElement("item")
            item5.setAttribute('id', 'roleB')
            item5.setAttribute('value', '')
            relation.appendChild(item5)
            # add relation
            xml.appendChild(relation)
        elif relationData['type'] == relationType.NASSOCIATION.name:
            relation1 = root.createElement(relationType.ASSOCIATION.value)
            relation1.setAttribute('id', relationData['t1'] + relationData['t2'])
            relation1.setAttribute('side_A', relationData['t1'])
            relation1.setAttribute('side_B', relationData['t2'])
            relation1.setAttribute('direction', '')
            # Relation item
            item1 = root.createElement("item")
            item1.setAttribute('id', 'name')
            item1.setAttribute('value', relationData['label'])
            relation1.appendChild(item1)
            item2 = root.createElement("item")
            item2.setAttribute('id', 'multiplicityA')
            item2.setAttribute('value', relationData['c1'])
            relation1.appendChild(item2)
            item3 = root.createElement("item")
            item3.setAttribute('id', 'multiplicityB')
            item3.setAttribute('value', relationData['c2'])
            relation1.appendChild(item3)
            item4 = root.createElement("item")
            item4.setAttribute('id', 'roleA')
            item4.setAttribute('value', '')
            relation1.appendChild(item4)
            item5 = root.createElement("item")
            item5.setAttribute('id', 'roleB')
            item5.setAttribute('value', '')
            relation1.appendChild(item5)
            # add relation1
            xml.appendChild(relation1)
            relation2 = root.createElement(relationType.ASSOCIATION.value)
            relation2.setAttribute('id', relationData['t1'] + relationData['t2'] + relationData['t3'])
            relation2.setAttribute('style', "dashed")
            relation2.setAttribute('side_A', relationData['t3'])
            relation2.setAttribute('side_B', relationData['t1'] + relationData['t2'])
            relation2.setAttribute('direction', '')
            # Relation item
            item6 = root.createElement("item")
            item6.setAttribute('id', 'multiplicityA')
            item6.setAttribute('value', relationData['c3'])
            relation2.appendChild(item6)
            item7 = root.createElement("item")
            item7.setAttribute('id', 'multiplicityB')
            item7.setAttribute('value', '')
            relation2.appendChild(item7)
            # add relation1
            xml.appendChild(relation2)
        elif relationData['type'] == relationType.GENERALISATION.name:
            relation = root.createElement(relationType.GENERALISATION.value)
            relation.setAttribute('id', relationData['t1'] + relationData['t2'])
            relation.setAttribute('side_A', relationData['t1'])
            relation.setAttribute('side_B', relationData['t2'])
            # Relation item
            item1 = root.createElement("item")
            item1.setAttribute('id', 'name')
            item1.setAttribute('value', relationData['label'])
            relation.appendChild(item1)
            item2 = root.createElement("item")
            item2.setAttribute('id', 'multiplicityA')
            item2.setAttribute('value', relationData['c1'])
            relation.appendChild(item2)
            item3 = root.createElement("item")
            item3.setAttribute('id', 'multiplicityB')
            item3.setAttribute('value', relationData['c2'])
            relation.appendChild(item3)
            # add relation
            xml.appendChild(relation)
        elif relationData['type'] == relationType.COMPOSITION.name:
            relation = root.createElement(relationType.COMPOSITION.value)
            relation.setAttribute('id', relationData['t1'] + relationData['t2'])
            relation.setAttribute('side_A', relationData['t1'])
            relation.setAttribute('side_B', relationData['t2'])
            # Relation item
            item1 = root.createElement("item")
            item1.setAttribute('id', 'name')
            item1.setAttribute('value', relationData['label'])
            relation.appendChild(item1)
            item2 = root.createElement("item")
            item2.setAttribute('id', 'multiplicityA')
            item2.setAttribute('value', relationData['c1'])
            relation.appendChild(item2)
            item3 = root.createElement("item")
            item3.setAttribute('id', 'multiplicityB')
            item3.setAttribute('value', relationData['c2'])
            relation.appendChild(item3)
            # add relation
            xml.appendChild(relation)
        elif relationData['type'] == relationType.AGGREGATION.name:
            relation = root.createElement(relationType.AGGREGATION.value)
            relation.setAttribute('id', relationData['t1'] + relationData['t2'])
            relation.setAttribute('side_A', relationData['t1'])
            relation.setAttribute('side_B', relationData['t2'])
            # Relation item
            item1 = root.createElement("item")
            item1.setAttribute('id', 'name')
            item1.setAttribute('value', relationData['label'])
            relation.appendChild(item1)
            item2 = root.createElement("item")
            item2.setAttribute('id', 'multiplicityA')
            item2.setAttribute('value', relationData['c1'])
            relation.appendChild(item2)
            item3 = root.createElement("item")
            item3.setAttribute('id', 'multiplicityB')
            item3.setAttribute('value', relationData['c2'])
            relation.appendChild(item3)
            # add relation
            xml.appendChild(relation)
        elif relationData['type'] == relationType.NairASSOCIATION.name:
            pass# vERSION 1.0.2
        else:
            pass

    # Return result.
    root.appendChild(xml)
    xml_str = root.toxml().replace("<?xml version=\"1.0\" ?>", "")
    return xml_str


class diagramTypeTag(Enum):
    UMLClassDiagram = "Class diagram"


class relationType(Enum):
    ASSOCIATION = "UMLAssociation"
    NASSOCIATION = "UMLClassEntityAssociation"
    NairASSOCIATION = "UMLNAssociation"
    RASSOCIATION = "UMLReflexiveAssociation"
    GENERALISATION = "UMLGeneralization"
    COMPOSITION = "UMLComposition"
    AGGREGATION = "UMLAggregation"


def diagramElementTag(val):
    if val == "UMLClassDiagram":
        return "UMLClass"
    else:
        return "Unkown"


def tableOffsetSetter(plainTableData):
    for table in plainTableData:
        tableItemList = table['attributes'] + table['methods']
        tableItemList.append(table['name'])
        table['width'] = (len(max(tableItemList, key=len)) * PIXEL_LETTER) + (2 * BOX_PADDING)
        table['height'] = (len(tableItemList) * PIXEL_LETTER) + (2 * BOX_PADDING)


def countLinkedNodes(relationList, nodeName, side):
    cpt = 0
    for i in relationList:
        if i[side] == nodeName:
            cpt += 1
    return cpt


def getRichNode(relationList):
    stat = dict()
    for relation in relationList:
        count = countLinkedNodes(relationList, relation['t1'], 't1')
        stat[relation['t1']] = {'count1': count, 'count2': 0}
    for relation in relationList:
        count = countLinkedNodes(relationList, relation['t2'], 't2')
        if relation['t2'] in stat.keys():
            stat[relation['t2']]['count2'] = count
        else:
            stat[relation['t2']] = {'count1': 0, 'count2': count}

    calculate = {'c1': [], 'c2': []}
    for d in stat.values():
        calculate['c1'].append(d['count1'])
        calculate['c2'].append(d['count2'])
    if len(calculate['c1']) != 0 and len(calculate['c2']) != 0:
        if max(calculate['c1']) > max(calculate['c2']):
            return 't1', list(stat.keys())[calculate['c1'].index(max(calculate['c1']))]
        elif max(calculate['c1']) < max(calculate['c2']):
            return 't2', list(stat.keys())[calculate['c2'].index(max(calculate['c2']))]
        else:
            return 't1', list(stat.keys())[calculate['c1'].index(max(calculate['c1']))]
    else:
        return None


class Node:
    def __init__(self, parent, child: list, label: str, x=0, y=0):
        self.parent = parent
        self.child = child
        self.x = x
        self.y = y
        self.preLimXCoord = 0
        self.modifier = None
        self.label = label

    def toString(self):
        print('\n-----node----->')
        print(self.child)
        print(self.x)
        print(self.y)
        print(self.preLimXCoord)

    def parent(self):
        return self.parent

    def firstChild(self):
        return self.child[0]

    def leftSibling(self):
        return None

    def rightSibling(self):
        return None

    def xCoord(self):
        return self.x

    def xCoord(self, val):
        self.x = val

    def yCoord(self):
        return self.y

    def yCoord(self, val):
        self.y = val

    def preLim(self):
        return self.preLimXCoord

    def preLim(self, val):
        self.preLimXCoord = val

    def modifier(self):
        return self.modifier

    def modifier(self, val):
        self.modifier = val

    def leftNeighbor(self):
        return None

    def isLeaf(self):
        # have to function logic
        return True


def nodeLeftMarginValue(x, separator, nChild):
    if nChild == 1:
        return x
    else:
        return int(x - ((nChild / 2) * separator))


def getTableOffset(tableName, all_node):
    for table in all_node:
        if table['name'] == tableName:
            return table['width'], table['width']


def setTableOffset(tableName, all_node, x, y):
    for table in all_node:
        if table['name'] == tableName:
            table['x'] = x
            table['y'] = y

X0 = 0

def treeNodePosition(all_node: list, relations: list, root_tag: tuple, parent=None, depth: int = 0, leftScale: int = 30) -> Node:
    # variables
    nodeRoot = Node(parent, [], root_tag[1], 0, depth)
    SEPARATION = 30
    LEFT_PADDING = 30
    nChild = 0
    nodeCursor = 0
    currentleftTab = [leftScale]
    currentNodeOffset = None

    # checking node child
    for i in range(len(relations)):
        # We're going to count current node child once
        if i == 0:
            for j in range(len(relations)):
                if relations[j][root_tag[0]] == root_tag[1]:
                    nChild += 1
                    currentNodeOffset = getTableOffset(relations[j][root_tag[0]], all_node)

        if relations[i][root_tag[0]] == root_tag[1]:
            symetricRootTag0 = 't1' if root_tag[0] == 't2' else 't2'
            # It means that we already draw all node and meet again root node
            if relations[i][symetricRootTag0] == getRichNode(relations)[1]:
                nChild -= 1
                break

            # Draw children recursively
            tuple_ = treeNodePosition(all_node, relations, (root_tag[0], relations[i][symetricRootTag0]), nodeRoot, depth + currentNodeOffset[1] + SEPARATION, currentleftTab[0])
            nodeRoot.child.append(tuple_[0])
            if tuple_[1][0] >= currentleftTab[0]:
                currentleftTab = tuple_[1]
            nodeCursor += 1

    # Assign posX in 2nd traversal
    if nChild == 0:
        # currentleftTab[0] = LEFT_PADDING
        nodeRoot.x = currentleftTab[0] + (SEPARATION*2)
    elif nChild == 1:
        nodeRoot.x = nodeRoot.child[0].x
        currentleftTab[0] = nodeRoot.x
    else:
        _startX = int(currentleftTab[0] - (currentleftTab[0]/nChild))
        for _node in nodeRoot.child:
            _node.x = _startX
            _startX = _startX + currentNodeOffset[0] + SEPARATION
        currentleftTab[0] = _startX

    # return new node
    # setTableOffset(root_tag[1], all_node, nodeRoot.x, nodeRoot.y)
    return nodeRoot, currentleftTab


def treeTraveler(tree: Node, all_node: list):
    # action
    setTableOffset(tree.label, all_node, tree.x, tree.y)

    # traveler
    for child in tree.child:
        treeTraveler(child, all_node)

def main(data):
    tableOffsetSetter(data['allNodes'])
    rootNodeTag = getRichNode(data['relation'])
    if rootNodeTag != None:
        tree, treeWidth = treeNodePosition(data['allNodes'], data['relation'], rootNodeTag)
        tree.x = abs(int(treeWidth[0]/2)-int(getTableOffset(tree.label, data['allNodes'])[0]/2))
        tree.x = 100
        tree.y = 40
        treeTraveler(tree, data['allNodes'])
    xml = xmlGenerator(diagramTypeTag.UMLClassDiagram, data)
    return xml
