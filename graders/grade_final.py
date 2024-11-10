from graders.foundry_grader import setup_repo, cleanup_repo, run_forge

def gradeFinal(submission):
    base_path = './graders/currsubmission'
    setup_repo(base_path,submission)
    
    # the following needs to be modified to reflect what we want to run.
    result = run_forge('script','script/Books.s.sol')
    grade = 30

    # these need to be refactored to a test.
    elements = [
        ['UBToken deployed at:','UBToken not Deployed'],
        ['UBToken.transfer confirmed','UBToken.transfer not confirmed'],
        ['UBNFT deployed at:','UBNFT not Deployed'],
        ['UBNFT.registerToken confirmed','UBNFT.registerToken not confirmed'],
        ['UBToken.approve confirmed','UBToken.approve not confirmed'],
        ['UBNFT.depositTokens confirmed','UBNFT.depositTokens not confirmed'],
        ['UBNFT.mint','UBNFT.mint not confirmed']
    ]
    
    msg = ''
    for element in elements:
        matches = re.findall(element[0],result)
        if matches:
            grade += 10
        else:
            msg += element[1] + '\n'
    
    return grade,msg
            





    
        
        

        