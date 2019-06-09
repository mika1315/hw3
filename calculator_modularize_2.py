def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def readMultiplication(line, index):
  token = {'type': 'MULTIPLICATION'}
  return token, index + 1


def readDivision(line, index):
  token = {'type': 'DIVISION'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readMultiplication(line, index)
    elif line[index] == '/':
      (token, index) = readDivision(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def firstEvaluate(tokens):
  flag = 'PLUS'
  number = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        flag = 'PLUS'
      elif tokens[index - 1]['type'] == 'MINUS':
        flag = 'MINUS'
      elif tokens[index - 1]['type'] == 'MULTIPLICATION':
        number *= tokens[index]['number']
        tokens[index]['number'] = number
        tokens[index - 2]['number'] = 0
        tokens[index - 1]['type'] = flag
      elif tokens[index - 1]['type'] == 'DIVISION':
        number /= tokens[index]['number']
        tokens[index]['number'] = number
        tokens[index - 2]['number'] = 0
        tokens[index - 1]['type'] = flag
      else:
        print('Invalid syntax')
        exit(1)
      number = tokens[index]['number']
    index += 1
  return tokens


def secondEvaluate(tokens):
  answer = 0
  # tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer


def test(line):
  first_tokens = tokenize(line)
  second_tokens = firstEvaluate(first_tokens)
  actualAnswer = secondEvaluate(second_tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("3.0+4*2-1/5")
  test("3.0+4*2*3-1/5/2")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  first_tokens = tokenize(line)
  # print(first_tokens)
  second_tokens = firstEvaluate(first_tokens)
  # print(second_tokens)
  answer = secondEvaluate(second_tokens)
  print("answer = %f\n" % answer)
