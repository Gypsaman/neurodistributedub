graders= {
    "SHA256": sha256_grader,
    "ECC": ecc_grader,
    "Wallet": wallet_grader,
}

def call_grader(assignment:str,submission:str) -> None:
    graders[assignment](submission)
    