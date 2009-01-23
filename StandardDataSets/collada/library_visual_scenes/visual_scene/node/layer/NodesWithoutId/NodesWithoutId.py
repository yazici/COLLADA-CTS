# Copyright (C) 2007 Khronos Group
# Available only to Khronos members.
# Distribution of this file or its content is strictly prohibited.

# See Core.Logic.FJudgementContext for the information
# of the 'context' parameter.
# [WARNING] this structure is subject to changes.
#

# This sample judging object does the following:
#
# JudgeBaseline: just verifies that the standard steps did not crash.
# JudgeExemplary: also verifies that the validation steps are not in error.
# JudgeSuperior: same as intermediate badge.

# Status value:
# -1000 : Initail status: test does not start yet.
# 0 : Failed
# 1 : Successful

from Core.Common.DOMParser import *
from Core.Common.CheckingModule import *

from xml.dom.minidom import parse, parseString
import os

# Please feed your node list here:
parentId = 'VisualSceneNode'
tagName = 'node'
attrLst = ['layer']

class SimpleJudgingObject:
    def __init__(self, status_basic_, status_intermediate_, status_advanced_, attrLst_):
        self.status_basic = status_basic_
        self.status_intermediate = status_intermediate_
        self.status_advanced = status_advanced_
        self.attrLst = attrLst_ # the attributes list where we will check.
        self.inputFilleName = ''
        self.outputFilleNameLst = []
        
    # This function is enough to test whether baked matrix is correct or not. through image comparison
    def JudgeBaseline(self, context):
        
        if len(self.attrLst) == 0:
            context.Log("Error: judging script doesn't have enough information about attributes.")
            return False
        
        # This is where you can test XML or force the comparison of image files
        # or any custom verification you want to do...
        if (context.HasStepCrashed()):
            context.Log("FAILED: Crashes during required steps.")
            return False
        else:
            context.Log("PASSED: No crashes.")

        # Check the required steps for positive results and that a rendering was done.
        if not context.HaveStepsPassed([ "Import", "Export", "Validate" ]):
            context.Log("FAILED: Import, export and validate steps must be present and successful.")
            self.status_basic = 0
            return False
        
        # Get the input file
        self.inputFilleName = context.GetAbsInputFilename(context.GetCurrentTestId())
        
        # Get the output file
        outputFilenames = context.GetStepOutputFilenames("Export")
        if len(outputFilenames) == 0:
            context.Log("FAILED: There are no export steps.")
            return False
        else:
            del self.outputFilleNameLst[:]
            self.outputFilleNameLst.extend( outputFilenames )
    
        context.Log("PASSED: Required steps executed and passed.")
        
        self.status_basic = 1
        return True
  
    # To pass intermediate you need to pass basic, this object could also include additional 
    # tests that were specific to the intermediate badge.
    def JudgeExemplary(self, context):
        if (self.status_basic == 1):
            
            testIO = DOMParserIO( self.inputFilleName, self.outputFilleNameLst )
            # load files and generate root
            testIO.Init()
            testPChecker = PresChecker(testIO.GetRoot(self.inputFilleName), testIO.GetRoot(self.outputFilleNameLst[0])  )
            resGetByTag = testPChecker.ResetElementsByTag(parentId,  tagName)
            
            if resGetByTag[0] == False:
                context.Log("Failed: layers are notpreserved.")
                context.Log("Message: " + resGetByTag[1])
                return False

            # Get all tags and then compare the attributes:
            resEleTags = testPChecker.checkElesAttribute( attrLst[0] )
            
            # release memory
            testIO.Delink()
            
            # flag for all test: only pass all, then we can give a bdage
            if resEleTags[0] == True:
                context.Log("Passed: all layers are preserved.")
                return True
            else:
                context.Log("Failed: layers are notpreserved.")
                context.Log("Message: " + resEleTags[1])
                return False
        else:
            context.Log("Did not pass basic test, not continue.")
            self.status_intermediate = 0
            return False        

    # To pass advanced you need to pass intermediate, this object could also include additional
    # tests that were specific to the advanced badge
    def JudgeSuperior(self, context):
        context.Log("N/A")
        return False

    # To pass FX you need to pass basic?
    # This object could also include additional
    # tests that were specific to the FX badges
    def JudgeFx(self, context):
        context.Log("N/A")
        return False

    # To pass advanced you need to pass intermediate, this object could also include additional
    # tests that were specific to the advanced badge
    def JudgePhysics(self, context):
        context.Log("N/A")
        return False

# This is where all the work occurs: "judgingObject" is an absolutely necessary token.
# The dynamic loader looks very specifically for a class instance named "judgingObject".
#
judgingObject = SimpleJudgingObject(-1000, -1000, -1000, attrLst);