valDict = {
  "type": "number",
  "value": 5,
}

minusDict = {
    "type": "BinOp",
    "operation": "MINUS",
    "left": {
        "type": "number",
        "value": 10
    },
    "right": {
        "type": "number",
        "value": 3
    }
}

variableExp = {
  "type": "Variable",
  "varName": "newVar",
}

# sample equality
eqExp = {
  "type": "Comparison",
  "left": {
      "type": "number",
      "value": 5,
    },
    "right": {
      "type": "number",
      "value": 5,
    },
}

letExp = {
  "type": "LetExp",
  "varName": "newVar",
  "val": {
        "type": "number",
        "value": 4
  },
  "body":{
    "type": "Comparison",
    "left": {
        "type": "Variable",
        "varName": "newVar",
        
      },
      "right": {
        "type": "Variable",
        "varName": "newVar",
        
    },
  }
}

condExp = {
  "type": "Condition",
  "cond": {
    "type": "Comparison",
    "left": {
      "type": "number",
      "value": 5,
    },
    "right": {
      "type": "number",
      "value": 5,
    },
  },
  "thenSide": {
    "type": "number",
    "value": 0,
  },
  "elseSide": {
    "type": "BinOp",
    "operation": "PLUS",
    "left": {
        "type": "number",
        "value": 4
    },
    "right": {
        "type": "number",
        "value": 10
    }
  }
}

knownFunctions = {}

functionDeclExp = {
  "type": "functionDeclExp",
  "name": "safeAdd",
  "formalArguments": ['first', 'second'],
  "body": {
    "type": "BinOp",
    "operation": "PLUS",
    "left": {
        "type": "Variable",
        "varName": "first",
    },
    "right": {
        "type": "Variable",
        "varName": "second",
    }
  },
  "scope": {
    "type": "functionCallExp",
    "name": "safeAdd",
    "arguments": [{
      "type": "BinOp",
      "operation": "MINUS",
      "left": {
          "type": "number",
          "value": 10
      },
      "right": {
          "type": "number",
          "value": 4
      }
    },
    {
    "type": "number",
    "value": 5,}]
    }
}

# functionCallExp = {
#   "type": "functionExp",
#   "name": "safeAdd",
#   "arguments": [1,2]
# }

class Environment:
  def __init__(self, binding, environment):
    self.binding = binding
    self.environment = environment

  def bind(self, binding):
    return Environment(binding, self)

  def lookup(self, name):
    try:
      if(name in self.binding):
        return self.binding[name]
      return self.environment.lookup(name)
    except:
      raise

def evalBinOp(val, e):
  if(val["operation"] == "PLUS"):
    return Evaluate(val["left"], e) + Evaluate(val["right"], e)
  elif(val["operation"] == "MINUS"):
    return Evaluate(val["left"], e) - Evaluate(val["right"], e)
  elif(val["operation"] == "TIMES"):
    return Evaluate(val["left"], e) * Evaluate(val["right"], e)
  elif(val["operation"] == "DIV"):
    return Evaluate(val["left"], e) / Evaluate(val["right"], e)

def Evaluate(eval, e):
  if(eval["type"] == "number"):
    return eval["value"]
  elif(eval["type"] == "BinOp"):
    return evalBinOp(eval, e)
  elif(eval["type"] == "Variable"):
    #eval["varName"] = Evaluate(eval["val"], e)
    return e.lookup(eval["varName"])
  elif(eval["type"] == "LetExp"):
    value = Evaluate(eval["val"], e)
    bindDict = {eval["varName"]: value}
    newE = e.bind(bindDict)
    return Evaluate(eval["body"], newE)
  elif(eval["type"] == "Comparison"):
    leftVar = Evaluate(eval["left"], e)
    rightVar = Evaluate(eval["right"], e)
    if(leftVar == rightVar):
      return True
    else:
      return False
  elif(eval["type"] == "Condition"):
    condition = Evaluate(eval["cond"], e)
    if(condition):
      return Evaluate(eval["thenSide"], e)
    else:
      return Evaluate(eval["elseSide"], e)
  elif(eval["type"] == "functionDeclExp"):
    def callFunc(actualValues):
      envThatKnowsTheArguments = e;
      for i in range(len(actualValues)):
        bindDict = {eval["formalArguments"][i]: actualValues[i]}
        envThatKnowsTheArguments = envThatKnowsTheArguments.bind(bindDict);
      return Evaluate(eval["body"], envThatKnowsTheArguments);
    knownFunctions[eval["name"]] = callFunc
    return Evaluate(eval["scope"], e)
  elif(eval["type"] == "functionCallExp"):
    actualValues = [None] * len(eval["arguments"])
    for i in range(len(eval["arguments"])):
      actualValues[i] = Evaluate(eval["arguments"][i], e)
    callingFunc = knownFunctions[eval["name"]]
    return callingFunc(actualValues)
    

eval = functionDeclExp
e = Environment(None, None)
output = Evaluate(eval, e)
print(output)

