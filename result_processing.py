import json as js
import sys
from os.path import basename, dirname

_, input_filename, output_filename, points_filename = sys.argv

# points is dict of string -> float with keys of "wheat", filenames of chaffs, & names corresponding to check block names in testsuite

visibility = "after_published"

with open(input_filename) as raw_f, open(points_filename) as points_f:
  raw, points = js.load(raw_f), js.load(points_f)

tests_passed = {}  # name -> bool  (keys same as for points)
tests_errored = []
chaff_names = set()
using_examplar = "wheat" in points

def gen_error(filename, message, examplar=False):
    if examplar:
        tests_errored.append({"name": filename, "score": 0, "max_score": points["examplar"][filename], "output": f"Error: {message}", "visibility": visibility})
    else:
        for name, score in filename.items():
            tests_errored.append({"name": name, "score": 0, "max_score": score, "output": f"Error: {message}", "visibility": visibility})

# populate testsuite_tests 
for test in raw:
    if "wheat" in test["code"]:
        if "Err" in test["result"]: 
            gen_error("wheat", test["result"]["Err"], True)
        elif len(test["result"]["Ok"]) == 0:
            gen_error("wheat", "Missing file", True)
        else:
            assert len(test["result"]["Ok"]) == 1
            check_block = test["result"]["Ok"][0]
            tests_passed["wheat"] = all([t["passed"] for t in check_block["tests"]])
    elif "chaff" in test["code"]:
        chaff_name = basename(test["code"]).replace(".arr", "")
        if "Err" in test["result"]: 
            gen_error(chaff_name, test["result"]["Err"], True)
        elif len(test["result"]["Ok"]) == 0:
            gen_error(chaff_name, "Missing file", True)
        else:
            assert len(test["result"]["Ok"]) == 1  # assuming student only wrote 1 check block in Examplar
            check_block = test["result"]["Ok"][0]
            tests_passed[chaff_name] = not(all([t["passed"] for t in check_block["tests"]]))
            chaff_names.add(chaff_name)
    else:  # test suite
        if "Err" in test["result"]: 
            gen_error(basename(dirname(test["tests"].split(";")[1])), test["result"]["Err"])
        else:
            for check_block in test["result"]["Ok"]:
                tests_passed[check_block["name"]] = all([t["passed"] for t in check_block["tests"]])

tests_scores = []  # list("name": str, "score": float, "max_score": float, "output": str, "visibility": "after_published"
for name in tests_passed:
    # assign points
    all_names_in_points = {i[0]: i[1] for i in {item for sublist in [i.items() for i in points.values()] for item in sublist}}
    if name not in all_names_in_points: 
        print(f"Test {name} not in points json")
    else:
        max_score = all_names_in_points[name]
        if name in chaff_names:  # we're dealing with a chaff
            score = all_names_in_points[name] if (tests_passed["wheat"] and tests_passed[name]) else 0
            message = "Passed all tests in this block!" if score == max_score else ("Wheat failed" if not(tests_passed["wheat"]) else "Failed some tests in this block")
            tests_scores.append({"name": name, "score": score, "max_score": max_score, "output": message, "visibility": visibility})
        else: 
            score = all_names_in_points[name] if tests_passed[name] else 0
            message = "Passed all tests in this block!" if score == max_score else "Failed some tests in this block"
            tests_scores.append({"name": name, "score": score, "max_score": max_score, "output": message, "visibility": visibility})
    
output = {"stdout_visibility": "hidden", "tests": tests_scores + tests_errored}
  
with open(output_filename, "w+") as f:
    js.dump(output, f)
