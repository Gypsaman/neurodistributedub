from grade_foundry import setup_repo, cleanup_repo, run_forge_test

def gradeFinal(submission):
    base_path = './graders/currsubmission'
    setup_repo(base_path,submission)
    result = run_forge_test()
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
            





    
        
        

        