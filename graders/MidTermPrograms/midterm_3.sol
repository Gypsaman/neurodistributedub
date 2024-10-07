
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct Exam {
        
        string name;
        uint256 score;
        uint256 student_id;
    }

    Exam public exam;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(string memory _name, uint256  _score, uint256 _student_id) {
        
        exam.name = _name;
        exam.score = _score;
        exam.student_id = _student_id;


        owner = msg.sender;

    }
    function update_score(uint256 _student_id) public onlyOwner {
        exam.student_id = _student_id;
    }

    function get_exam() public view returns (Exam memory) {
        return exam;
    }

}
    