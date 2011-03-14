# Copyright (C) 2007 Khronos Group
# Available only to Khronos members.
# Distribution of this file or its content is strictly prohibited.

# See Core.Logic.FJudgementContext for the information
# of the 'context' parameter.

# This sample judging object does the following:
#
# JudgeBaseline: just verifies that the standard steps did not crash.
# JudgeSuperior: also verifies that the validation steps are not in error.
# JudgeExemplary: same as intermediate badge.

# We import an assistant script that includes the common verifications
# methods. The assistant buffers its checks, so that running them again
# does not incurs an unnecessary performance hint.
from StandardDataSets.scripts import JudgeAssistant

# Please feed your node list here:
tagLst = [['library_effects', 'effect', 'profile_COMMON', 'technique', 'blinn', 'transparent', 'color'], ['library_effects', 'effect', 'profile_COMMON', 'newparam', 'float4'], ['library_effects', 'effect', 'newparam', 'float4']]
tagLst2 = [['library_effects', 'effect', 'profile_COMMON', 'technique', 'blinn', 'transparent', 'color'], ['library_effects', 'effect', 'profile_COMMON', 'technique', 'blinn', 'transparency', 'float']]
attrName = ''
attrVal = ''
dataToCheck = ['1 1 1 1', '0.7']

class SimpleJudgingObject:
    def __init__(self, _tagLst, _attrName, _attrVal, _data, _tagLst2):
        self.tagList = _tagLst
        self.tagList2 = _tagLst2
        self.attrName = _attrName
        self.attrVal = _attrVal
        self.dataToCheck = _data
        self.status_baseline = False
        self.status_superior = False
        self.status_exemplary = False
        self.__assistant = JudgeAssistant.JudgeAssistant()

    def checkTransparent(self, context):
        if ( self.__assistant.ElementDataPreservedIn(context, self.tagList, "float", False) ):
            context.Log("PASSED: Transparent value is preserved.")
            return True
        else:
            if ( self.__assistant.ElementDataCheck(context, self.tagList2[0], self.dataToCheck[0], "float", False) and 
                 self.__assistant.ElementDataCheck(context, self.tagList2[1], self.dataToCheck[1], "float", False) ):
                context.Log("PASSED: Transparent alpha value is preserved in transparency element.")
                return True
        
        context.Log("FAILED: Transparent value is not preserved.")
        return False
        
    def JudgeBaseline(self, context):
        # No step should not crash
        self.__assistant.CheckCrashes(context)
        
        # Import/export/validate must exist and pass, while Render must only exist.
        self.__assistant.CheckSteps(context, ["Import", "Export", "Validate"], ["Render"])
        
        self.status_baseline = self.__assistant.GetResults()
        return self.status_baseline
  
    # To pass intermediate you need to pass basic, this object could also include additional 
    # tests that were specific to the intermediate badge.
    def JudgeSuperior(self, context):
        # if baseline fails, no point in further checking
        if (self.status_baseline == False):
            self.status_superior = self.status_baseline
            return self.status_superior
        
        # Compare the rendered images between import and export
        # Then compare images against color black reference test for equivalence
        # Then compare images against alpha 0 reference test for non-equivalence
        # Last, check for preservation of element data
        if ( self.__assistant.CompareRenderedImages(context) ):
            if ( self.__assistant.CompareImagesAgainst(context, "_ref_blinn_transparent_aone_black", None, None, 5, True, True) ):
                if ( self.__assistant.CompareImagesAgainst(context, "_ref_blinn_transparent_aone_alpha0", None, None, 5, True, False) ):
                    self.status_baseline = self.checkTransparent(context)
                    return self.status_baseline
        
        self.status_superior = self.__assistant.DeferJudgement(context)
        return self.status_superior 
            
    # To pass advanced you need to pass intermediate, this object could also include additional
    # tests that were specific to the advanced badge
    def JudgeExemplary(self, context):
        self.status_exemplary = self.status_superior
        return self.status_exemplary 
       
# This is where all the work occurs: "judgingObject" is an absolutely necessary token.
# The dynamic loader looks very specifically for a class instance named "judgingObject".
#
judgingObject = SimpleJudgingObject(tagLst, attrName, attrVal, dataToCheck, tagLst2);
