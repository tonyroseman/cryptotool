import json
import copy

class SettingsModule:
    opstr = [' > ',' < ',' >= ', ' <= ']
    isAdvanced = False
    alldata = []
    treealldata = []
    operator_string = ['AND', 'OR']
    def __init__(self, settingdata=None):
        data = {}
        
        self.alldata = []
        self.treealldata = []
        
        if settingdata is not None:
            
            self.alldata = settingdata
            self.treealldata = copy.deepcopy(settingdata)
            self.makeTreeData(self.treealldata)
        else:
            data['text'] = ' Advanced Settings'                                    
            data['nodes'] = []
            data['id'] = '0'
            data['level'] = 0
            data['index'] = 0
            data['isLeaf'] = 0            
            data['parent'] = '-1'
            self.alldata.append(data)
            self.treealldata = copy.deepcopy(self.alldata)
            self.makeTreeData(self.treealldata)
    def getRawData(self):
        return self.alldata
    def getTreeData(self):
        return self.treealldata
    def makeTreeData(self, nodes):
        for node in nodes:
            if node['isLeaf'] == 0:
                node['color'] = '#ff0000'
                node['icon'] = 'glyphicon glyphicon-tags'
            if 'nodes' in node:
                node['nodes'] = self.makeTreeData(node['nodes'])
        return nodes
    def getExpression(self):
        return self.makeExpression(self.alldata[0])
    
    def makeExpression(self, node):
        expression = ""
        if node['isLeaf'] == 1:
            print(node['text'])
            return node['text']
        else:
            if 'nodes' in node:
                expressions = []
                for pnode in node['nodes']:
                    expressions.append(self.makeExpression(pnode))
                if len(node['nodes']) > 0:
                    if node['id'] == '0':
                        return expressions[0]
                    else:
                        expression = "(" + expressions[0]
                        for i in range(1,len(expressions)):
                            if expressions[i] != "":
                                expression = expression + " " + self.operator_string[int(node['cond_op'])-1] + " " + expressions[i]
                        expression = expression + " )"   
                        print(expression) 
                        return expression
        print(expression)
        return expression
        
    def findNode(self, nodeid, startNode):
        
        
        if startNode['id'] == nodeid:
            return startNode
        else:
            if 'nodes' in startNode:
                for node in startNode['nodes']:
                    retNode = self.findNode(nodeid, node)
                    if retNode is not None:
                        return retNode
        return None
        

    def changeGroupOperator(self,groupid, operator):
        for node in self.alldata:
            groupNode = self.findNode(groupid, node)
            if groupNode is not None:
                groupNode['cond_op'] = operator
                groupNode['text'] = ' ' + self.operator_string[int(operator)-1] + " Group"
                return 1
        return 0
    def deleteGroup(self,groupid):
        for node in self.alldata:
            groupNode = self.findNode(groupid, node)
            if groupNode is not None:
                if groupNode['id'] == '0':
                    return 1
                else:
                    for pnode in self.alldata:
                        parentNode = self.findNode(groupNode['parent'], pnode)
                        if parentNode is not None:
                            nodes = parentNode['nodes']
                            del nodes[groupNode['index']]
                            index = 0
                            for node in nodes:
                                node['id'] = node['parent'] + "_" + str(index)
                                node['index'] = index
                                index += 1
                            parentNode['nodes'] = nodes
                            return 1
                
                    
        return 0
    def deleteCondition(self,condid):
        for node in self.alldata:
            condNode = self.findNode(condid, node)
            if condNode is not None:
                if condNode['id'] == '0':
                    return 1
                else:
                    for pnode in self.alldata:
                        parentNode = self.findNode(condNode['parent'], pnode)
                        if parentNode is not None:
                            nodes = parentNode['nodes']
                            del nodes[condNode['index']]
                            index = 0
                            for node in nodes:
                                node['id'] = node['parent'] + "_" + str(index)
                                node['index'] = index
                                index += 1
                            parentNode['nodes'] = nodes
                            return 1
                
                    
        return 0
    def addGroup(self,groupid, operator):
        for node in self.alldata:
            groupNode = self.findNode(groupid, node)
            if groupNode is not None:
                if groupNode['isLeaf'] == 0:
                    if 'nodes' in groupNode:
                        nodes = groupNode['nodes']
                        newGroupNode = {}
                        newGroupNode['text'] = ' ' + self.operator_string[int(operator)-1] + " Group"
                        newGroupNode['parent'] = groupid            
                        newGroupNode['nodes'] = []
                        newGroupNode['id'] = groupid + "_" + str(len(nodes))
                        newGroupNode['level'] = groupNode['level'] + 1
                        newGroupNode['index'] = len(nodes)
                        newGroupNode['isLeaf'] = 0
                        newGroupNode['cond_op'] = operator
                        nodes.append(newGroupNode)
                        groupNode['nodes'] = nodes
                    else:
                        nodes = []
                        newGroupNode = {}
                        newGroupNode['text'] = ' ' + self.operator_string[int(operator)-1] + " Group"
                        newGroupNode['parent'] = groupid            
                        newGroupNode['nodes'] = []
                        newGroupNode['id'] = groupid + "_" + str(len(nodes))
                        newGroupNode['level'] = groupNode['level'] + 1
                        newGroupNode['index'] = len(nodes)
                        newGroupNode['isLeaf'] = 0
                        newGroupNode['cond_op'] = operator
                        nodes.append(newGroupNode)
                        groupNode['nodes'] = nodes
                    return 1
        return 0
    def addCondition(self,groupid, cond_type, glt, cvalue):
        for node in self.alldata:
            groupNode = self.findNode(groupid, node)
            if groupNode is not None:
                if groupNode['isLeaf'] == 0:
                    if 'nodes' in groupNode:
                        nodes = groupNode['nodes']
                        newCondition = {}
                        newCondition['id'] = groupid + "_" + str(len(nodes))
                        newCondition['level'] = groupNode['level'] + 1
                        newCondition['index'] = len(nodes)
                        newCondition['parent'] = groupid
                        newCondition['key'] = cond_type
                        newCondition['op'] = int(glt)
                        newCondition['value'] = float(cvalue)
                        if cond_type == 'mc':
                            newCondition['text'] = ' ' + 'market cap' + self.opstr[newCondition['op']-1] + str(newCondition['value'])
                        else:
                            newCondition['text'] = ' ' + cond_type + self.opstr[newCondition['op']-1] + str(newCondition['value'])
                        newCondition['isLeaf'] = 1
                        
                        nodes.append(newCondition)
                        groupNode['nodes'] = nodes
                    else:
                        nodes = []
                        newCondition = {}
                        newCondition['id'] = groupid + "_" + str(len(nodes))
                        newCondition['level'] = groupNode['level'] + 1
                        newCondition['index'] = len(nodes)
                        newCondition['parent'] = groupid
                        newCondition['key'] = cond_type
                        newCondition['op'] = int(glt)
                        newCondition['value'] = float(cvalue)
                        if cond_type == 'mc':
                            newCondition['text'] = ' ' + 'market cap' + self.opstr[newCondition['op']-1] + str(newCondition['value'])
                        else:
                            newCondition['text'] = ' ' + cond_type + self.opstr[newCondition['op']-1] + str(newCondition['value'])
                        newCondition['isLeaf'] = 1
                        
                        nodes.append(newCondition)
                        groupNode['nodes'] = nodes
                    return 1
        return 0
    
    def changeCondition(self,condid, cond_type, glt, cvalue):
        for node in self.alldata:
            condNode = self.findNode(condid, node)
            if condNode is not None:
                if condNode['isLeaf'] == 1:
                    condNode['key'] = cond_type
                    condNode['op'] = int(glt)
                    condNode['value'] = float(cvalue)
                    if cond_type == 'mc':
                        condNode['text'] = ' ' + 'market cap' + self.opstr[condNode['op']-1] + str(condNode['value'])
                    else:
                        condNode['text'] = ' ' + cond_type + self.opstr[condNode['op']-1] + str(condNode['value'])
                        
                    return 1
        return 0
    def makeConditionToGroup(self,condid, operator):
        for node in self.alldata:
            condNode = self.findNode(condid, node)
            if condNode is not None:
                if condNode['id'] == '0':
                    return 1
                else:
                    for pnode in self.alldata:
                        parentNode = self.findNode(condNode['parent'], pnode)
                        if parentNode is not None:
                            nodes = parentNode['nodes']
                            newGroupNode = {}
                            newGroupNode['text'] = ' ' + self.operator_string[int(operator)-1] + " Group"
                            newGroupNode['parent'] = parentNode['id']            
                            newGroupNode['nodes'] = []
                            newGroupNode['id'] = condNode['id']
                            newGroupNode['level'] = condNode['level']
                            newGroupNode['index'] = condNode['index']
                            newGroupNode['isLeaf'] = 0
                            newGroupNode['cond_op'] = operator
                            condNode['id'] = newGroupNode['id'] + "_" + "0"
                            condNode['level'] = condNode['level'] + 1
                            condNode['index'] = 0
                            newGroupNode['nodes'].append(condNode)
                            nodes[newGroupNode['index']] = newGroupNode
                            
                            parentNode['nodes'] = nodes
                            return 1
        return 0
            
    


                        



