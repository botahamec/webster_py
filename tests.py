"""
Tests for Webster 0.2
"""

from webster_py import RuleType, Rule, Property, Definition, Thing, Webster

def test(name, result, expected):
	"""
	Tests if a given value is equivalent to the expected value
	Example Usage: test("concatenation", hello", "he" + "llo")
	Returns true if the test passed, false otherwise
	"""

	if result == expected:
		print("\033[32m" + name + ": PASSED" + "\033[0m")
		return True
	else:
		print("\033[91m" + name + ": FAILED")
		print("\033[91m" + "\tExpected:", expected)
		print("\033[91m" + "\tResult:", result, "\033[0m")
		return False

# -----------------------------------------------------------------------------
# -------------------------- RULE TESTS ---------------------------------------
# -----------------------------------------------------------------------------

# test Rule.match(value) when Rule.rule_type == RuleType.IS
def rule_match_is():
	test("Rule IS 1", Rule(RuleType.IS, "Hello").match("Hello"), True)
	test("Rule IS 2", Rule(RuleType.IS, "Hello").match("World"), False)

# test Rule.match(value) when Rule.rule_type == RuleType.GREATER
def rule_match_greater():
	greater_rule = Rule(RuleType.GREATER, 3) # greater than 3
	test("Rule GREATER 1", greater_rule.match(5), True)
	test("Rule GREATER 2", Rule(RuleType.GREATER, 3).match(1), False)

# test Rule.match(value) when Rule.rule_type == RuleType.LESS
def rule_match_less():
	less_rule = Rule(RuleType.LESS, 10) # less than 10
	test("Rule LESS 1", less_rule.match(1), True)
	test("Rule LESS 2", less_rule.match(12), False)

# test Rule.match(value) when Rule.rule_type == RuleType.AND
def rule_match_and():
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule]) # between 3 & 10
	test("Rule AND 1", and_rule.match(7), True)
	test("Rule AND 2", and_rule.match(0), False)
	test("Rule AND 3", and_rule.match(15), False)

# test Rule.match(value) when Rule.rule_type == RuleType.OR
def rule_match_or():
	greater_rule = Rule(RuleType.GREATER, 3)
	or_rule = Rule(RuleType.OR, [Rule(RuleType.IS, 3), greater_rule]) # >= 3
	test("Rule OR 1", or_rule.match(3), True)
	test("Rule OR 2", or_rule.match(5), True)
	test("Rule OR 3", or_rule.match(-3), False)

# test Rule.match(value) when Rule.rule_type == RuleType.OR
def rule_match_contain():
	contain_rule = Rule(RuleType.CONTAIN, 'h') # contains letter h
	test("Rule CONTAIN 1", contain_rule.match("hello"), True)
	test("Rule CONTAIN 2", contain_rule.match("world"), False)

# test Rule.match(value) when Rule.rule_type == RuleType.XOR
def rule_match_xor():
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])
	test("Rule XOR 1", xor_rule.match("world"), True)
	test("Rule XOR 2", xor_rule.match("help"), True)
	test("Rule XOR 3", xor_rule.match("hello"), False)
	test("Rule XOR 4", xor_rule.match("animal"), False)

# test Rule.match(value) when Rule.rule_type == RuleType.NOT
def rule_match_not():
	not_rule = Rule(RuleType.NOT, Rule(RuleType.IS, 6)) # not 6
	test("Rule NOT 1", not_rule.match(3), True)
	test("Rule NOT 2", not_rule.match(6), False)

# -----------------------------------------------------------------------------
# -------------------------- METHOD TESTS -------------------------------------
# -----------------------------------------------------------------------------

# tests Rule.__init__()
def init_rule():
	rule = Rule(RuleType.GREATER, 5)
	test("Rule Construction Type", rule.rule_type, RuleType.GREATER)
	test("Rule Construction Value", rule.value, 5)

# tests Rule.__eq__()
def rule_eq():
	rule1 = Rule(RuleType.GREATER, 5)
	rule2 = Rule(RuleType.GREATER, 5)
	rule3 = Rule(RuleType.GREATER, 3)
	rule4 = Rule(RuleType.LESS, 5)
	test("Rule Equality", rule1 == rule2, True)
	test("Rule Inequality 1", rule1 == rule3, False)
	test("Rule Inequality 2", rule1 == rule4, False)

# tests Rule.match(value)
def rule_match():
	rule_match_is()
	rule_match_greater()
	rule_match_less()
	rule_match_and()
	rule_match_or()
	rule_match_contain()
	rule_match_xor()
	rule_match_not()

# tests Property.__init__()
def init_property():
	rule = Rule(RuleType.GREATER, 5)
	prop = Property("count", rule)
	test("Property Construction Name", prop.name, "count")
	test("Property Construction Rule", prop.rule, rule)

# tests Property.__eq__()
def property_eq():
	rule = Rule(RuleType.GREATER, 5)
	prop1 = Property("count", rule)
	prop2 = Property("count", rule)
	prop3 = Property("name", rule)
	prop4 = Property("count", Rule(RuleType.LESS, 10))
	test("Property Equality", prop1 == prop2, True)
	test("Property Inequality 1", prop1 == prop3, False)
	test("Property Inequality 2", prop1 == prop4, False)

# tests Property.match(value)
def property_match():
	rule = Rule(RuleType.GREATER, 5)
	prop = Property("count", rule)
	test("Property Match 1", prop.match(7), True)
	test("Property Match 1", prop.match(5), False)

# tests Definition.__init__()
def init_definition():

	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# define a definition for testing
	definition = Definition("TestyDef", [name_prop, valu_prop])

	# the expected value of definition.prop
	exp_prop = {"Name": name_prop, "Value": valu_prop}

	test("Definition Construction Name", definition.name, "TestyDef")
	test("Definition Construction Properties", definition.props, exp_prop)

# tests Definition.__eq__()
def definition_eq():

	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# run the test
	def1 = Definition("TestyDef", [name_prop, valu_prop])
	def2 = Definition("TestyDef", [name_prop, valu_prop])
	def3 = Definition("TestDef", [name_prop, valu_prop])
	def4 = Definition("TestyDef", [name_prop])
	test("Definition Equality", def1 == def2, True)
	test("Definition Inequality 1", def1 == def3, False)
	test("Definition Inequality 2", def1 == def4, False)

# tests Definition.match(Thing)
def definition_match():

	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# define a definition for testing
	definition = Definition("TestyDef", [name_prop, valu_prop])

	# define a thing for testing
	thing = Thing("TestyThingy", attributes={"Name": "Hello", "Value": 4})
	test("Definition Match 1", definition.match(thing), True)
	thing = Thing("TestyThingy", attributes={"Name": "hello", "Value": 4})
	test("Definition Match 2", definition.match(thing), False)
	thing = Thing("TestyThingy", attributes={"Name": "Hello", "Value": 3})
	test("Definition Match 3", definition.match(thing), False)

# tests Thing.__init()
def init_thing():

	# test thing.name
	thing = Thing("TestyThingy")
	test("Thing Construction ID", thing.identifier, "TestyThingy")

	# test thing.attrs and thing.definition
	attrs = {"Name": "Hello", "Value": 3}
	thing = Thing("TestyThingy", attributes=attrs, definition="TestyDef")
	test("Thing Construction Properties", thing.attrs, attrs)
	test("Thing Construction Definition", thing.definition, "TestyDef")

# tests Thing.__eq__()
def thing_eq():
	attrs = {"Name": "Hello", "Value": 3}
	thing1 = Thing("TestyThingy", attributes=attrs, definition="TestyDef")
	thing2 = Thing("TestyThingy", attributes=attrs, definition="TestyDef")
	thing3 = Thing("SuperThing", attributes=attrs, definition="TestyDef")
	thing4 = Thing("TestyThing", definition="TestyDef")
	thing5 = Thing("TestyThing", attributes=attrs)
	test("Thing Equality", thing1 == thing2, True)
	test("Thing Inequality 1", thing1 == thing3, False)
	test("Thing Inequality 2", thing1 == thing4, False)
	test("Thing Inequality 3", thing1 == thing5, False)

# tests Webster.__init__()
def init_webster():

	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# define a definition for testing
	definition = Definition("TestyDef", [name_prop, valu_prop])

	# define a thing
	attrs = {"Name": "Hello", "Value": 3}
	thing = Thing("TestyThingy", attributes=attrs, definition="TestyDef")

	# defines Webster
	webster = Webster(brain=[thing], dictionary=[definition])

	# tests for the correct values
	dict_test = webster.dictionary["TestyDef"]
	test("Webster Construction Dictionary", dict_test, definition)
	test("Webster Construction Brain", webster.brain["TestyThingy"], thing)

# tests Webster.__eq__()
def webster_eq():

	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# define a definition for testing
	definition = Definition("TestyDef", [name_prop, valu_prop])

	# define a thing
	attrs = {"Name": "Hello", "Value": 3}
	thing = Thing("TestyThingy", attributes=attrs, definition="TestyDef")

	# defines Webster
	webster1 = Webster(brain=[thing], dictionary=[definition])
	webster2 = Webster(brain=[thing], dictionary=[definition])
	webster3 = Webster(dictionary=[definition])
	webster4 = Webster(brain=[thing])
	test("Webster Equality", webster1 == webster2, True)
	test("Webster Inequality 1", webster1 == webster3, False)
	test("Webster Inequality 2", webster1 == webster4, False)

# tests Webster.get_definition(name)
def webster_get_definition():

	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# define a definition for testing
	definition = Definition("TestyDef", [name_prop, valu_prop])

	# defines Webster
	webster = Webster(dictionary=[definition])

	# tests to get the definition
	test_result = webster.get_definition("TestyDef")
	test("Webster Get Definition", test_result, definition)

# tests Webster.get_thing(identifier)
def webster_get_thing():

	# define a thing
	attrs = {"Name": "Hello", "Value": 3}
	thing = Thing("TestyThingy", attributes=attrs)

	webster = Webster(brain=[thing]) # define Webster

	# run test
	test("Webster Get Thing", webster.get_thing("TestyThingy"), thing)

# tests Webster.add_definition()
def webster_add_definition():

	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# runs test
	definition = Definition("TestyDef", [name_prop, valu_prop])
	webster = Webster()
	webster.add_definition("TestyDef", [name_prop, valu_prop])
	result = webster.get_definition("TestyDef")
	test("Webster Add Definition", result, definition)

# tests Webster.add_thing()
def webster_add_thing():

	# define a thing
	attrs = {"Name": "Hello", "Value": 3}
	thing = Thing("TestyThingy", attributes=attrs)

	# run the test
	webster = Webster()
	webster.add_thing("TestyThingy", attributes=attrs)
	test("Webster Add Thing", webster.get_thing("TestyThingy"), thing)

# tests Webster.get_property()
def webster_get_prop():

	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# run test
	webster = Webster()
	webster.add_definition("TestyDef", [name_prop, valu_prop])
	result = webster.get_property("TestyDef", "Name")
	test("Webster Get Property", result, name_prop)

# tests Webster.get_rule()
def webster_get_rule():
	
	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# run test
	webster = Webster()
	webster.add_definition("TestyDef", [name_prop, valu_prop])
	result = webster.get_rule("TestyDef", "Name")
	test("Webster Get Rule", result, xor_rule)

# tests Webster.get_attribute()
def webster_get_attr():
	attrs = {"Name": "Hello", "Value": 3}
	webster = Webster()
	webster.add_thing("TestyThingy", attributes=attrs)
	result = webster.get_attribute("TestyThingy", "Name")
	test("Webster Get Attribute", result, "Hello")

# tests Webster.set_property_rule()
def webster_set_rule():
	
	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])
	new_rule = Rule(RuleType.IS, "Hello")

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# run test
	webster = Webster()
	webster.add_definition("TestyDef", [name_prop, valu_prop])
	webster.set_property_rule("TestyDef", "Name", new_rule)
	test("Webster Set Rule", webster.get_rule("TestyDef", "Name"), new_rule)

# tests Webster.add_property()
def webster_add_prop():
	
	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# run test
	webster = Webster()
	webster.add_definition("TestyDef", [name_prop])
	webster.add_property("TestyDef", "Value", and_rule)
	result = webster.get_property("TestyDef", "Value")
	test("Webster Add Property", result, valu_prop)

# tests Webster.set_attribute()
def webster_set_attr():
	attrs = {"Name": "Hello"}
	webster = Webster()
	webster.add_thing("TestyThingy", attributes=attrs)
	webster.set_attribute("TestyThingy", "Value", 3)
	result = webster.get_attribute("TestyThingy", "Value")
	test("Webster Set Attribute", result, 3)

# tests Webster.has_property()
def webster_has_prop():
	
	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# run test
	webster = Webster()
	webster.add_definition("TestyDef", [name_prop, valu_prop])
	result1 = webster.has_property("TestyDef", "Name")
	result2 = webster.has_property("TestyDef", "Count")
	test("Webster Has Property 1", result1, True)
	test("Webster Has Property 2", result2, False)

# tests Webster.has_attribute()
def webster_has_attr():
	attrs = {"Name": "Hello", "Value": 3}
	webster = Webster()
	webster.add_thing("TestyThingy", attributes=attrs)
	result1 = webster.has_attribute("TestyThingy", "Name")
	result2 = webster.has_attribute("TestyThingy", "Count")
	test("Webster Has Attribute 1", result1, True)
	test("Webster Has Attribute 2", result2, False)

# tests Webster.has_definition()
def webster_has_def():

	# define rules to use
	greater_rule = Rule(RuleType.GREATER, 3)
	less_rule = Rule(RuleType.LESS, 10)
	and_rule = Rule(RuleType.AND, [greater_rule, less_rule])
	contain_rule = Rule(RuleType.CONTAIN, 'h')
	xor_rule = Rule(RuleType.XOR, [contain_rule, Rule(RuleType.CONTAIN, 'o')])

	# define properties to use
	name_prop = Property("Name", xor_rule)
	valu_prop = Property("Value", and_rule)

	# define a definition for testing
	definition = Definition("TestyDef", [name_prop, valu_prop])

	# define a thing
	attrs1 = {"Name": "Hello", "Value": 5}
	attrs2 = {"Name": "hello", "Value": 1}
	thing1 = Thing("Thing 1", attributes=attrs1, definition="TestyDef")
	thing2 = Thing("Thing 2", attributes=attrs2)
	thing3 = Thing("Thing Red", attributes=attrs2, definition="TestyDef")
	thing4 = Thing("Thing Blue", attributes=attrs1)
	brain = [thing1, thing2, thing3, thing4]

	# runs test
	webster = Webster(brain=brain, dictionary=[definition])
	result1 = webster.has_definition("Thing 1", "TestyDef")
	result2 = webster.has_definition("Thing 2", "TestyDef")
	result3 = webster.has_definition("Thing Red", "TestyDef")
	result4 = webster.has_definition("Thing Blue", "TestyDef")
	test("Webster Has Definition 1", result1, True)
	test("Webster Has Definition 2", result2, False)
	test("Webster Has Definition 3", result3, True)
	test("Webster Has Definition 4", result4, True)

# -----------------------------------------------------------------------------
# -------------------------- CLASS TESTS --------------------------------------
# -----------------------------------------------------------------------------

# tests RuleType enumerator
def rule_type_enum():
	test("RuleType Is", RuleType.IS, RuleType.IS)

# runs all tests for the Rule Class
def rule_tests():
	init_rule()
	rule_eq()
	rule_match()

# runs all tests for the Property class
def prop_tests():
	init_property()
	property_eq()
	property_match()

# runs all tests for the Definition class
def def_tests():
	init_definition()
	definition_eq()
	definition_match()

# runs all tests for the Thing class
def thing_tests():
	init_thing()
	thing_eq()

# runs all tests for the Webster class
def webster_tests():
	init_webster()
	webster_eq()
	webster_get_definition()
	webster_get_thing()
	webster_add_definition()
	webster_add_thing()
	webster_get_prop()
	webster_get_rule()
	webster_get_attr()
	webster_set_rule()
	webster_add_prop()
	webster_set_attr()
	webster_has_prop()
	webster_has_attr()
	webster_has_def()

# -----------------------------------------------------------------------------
# -------------------------- RUN ALL TESTS ------------------------------------
# -----------------------------------------------------------------------------

def run_all_tests():
	rule_type_enum()
	rule_tests()
	prop_tests()
	def_tests()
	thing_tests()
	webster_tests()

if __name__ == "__main__":
	run_all_tests()
