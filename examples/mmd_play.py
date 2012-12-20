from serializer.simpl_types_scope import SimplTypesScope
from utils.format import Format
import json


print "Testing"

#scope_location = "../test/mmd/mmd_repo_scope.json"
scope_location = "../test/mmd/mmd_repo_scope_lite.json"

blah = json.load(open(scope_location))

#scope = SimplTypesScope(Format.JSON, scope_location)




#person = scope.SimplType("Student")
#person.name = "Bob"
#person.stuNum = 3434#All of the different names are a little confusing, we should think about making an anatomy chart
#person.arbitrary = "Bob"#will not serialize
#print scope.serialize(person, Format.JSON)