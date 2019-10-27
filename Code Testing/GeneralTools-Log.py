"""
Test output of GeneralTools's log function.
"""
import GeneralTools as Tools

# Test emancipated calling; no class or function; "raw file execution"
Tools.log('error', Tools.LEVEL_ERROR)
Tools.log('warn', Tools.LEVEL_WARN)
Tools.log('normal', Tools.LEVEL_NORMAL)
Tools.log('explict normal', Tools.LEVEL_NORMAL)
Tools.log('ok', Tools.LEVEL_OK)


# Test divorced calling; no class | only function
def function_test():
    Tools.log('error', Tools.LEVEL_ERROR)
    Tools.log('warn', Tools.LEVEL_WARN)
    Tools.log('normal', Tools.LEVEL_NORMAL)
    Tools.log('explict normal', Tools.LEVEL_NORMAL)
    Tools.log('ok', Tools.LEVEL_OK)


function_test()


class CodeTester:
    # Test divorced calling; no method | only class
    Tools.log('error', Tools.LEVEL_ERROR)
    Tools.log('warn', Tools.LEVEL_WARN)
    Tools.log('normal', Tools.LEVEL_NORMAL)
    Tools.log('explict normal', Tools.LEVEL_NORMAL)
    Tools.log('ok', Tools.LEVEL_OK)

    # Test ideal calling; both class and method
    def method_test(self):
        Tools.log('error', Tools.LEVEL_ERROR)
        Tools.log('warn', Tools.LEVEL_WARN)
        Tools.log('normal', Tools.LEVEL_NORMAL)
        Tools.log('explict normal', Tools.LEVEL_NORMAL)
        Tools.log('ok', Tools.LEVEL_OK)

    method_test(None)
