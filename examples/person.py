from serializer.simpl_types_scope import SimplTypesScope
from utils.format import Format

print "Testing"

scope_location = "../test/test_scopes_and_instances/personDirectory_scope.json"

scope = SimplTypesScope(Format.JSON, scope_location)
person = scope.SimplType("Student")

person.name = "Bob"
person.stuNum = 3434#All of the different names are a little confusing, we should think about making an anatomy chart
person.arbitrary = "Bob"#will not serialize
print scope.serialize(person, Format.JSON)