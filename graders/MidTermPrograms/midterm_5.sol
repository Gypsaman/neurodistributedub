
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct Movie {
        
        string title;
        string director;
        uint256 year;
    }

    Movie public movie;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(string memory _title, string memory _director, uint256 _year) {
        
        movie.title = _title;
        movie.director = _director;
        movie.year = _year;


        owner = msg.sender;

    }
    function update_year(uint256 _year) public onlyOwner {
        movie.year = _year;
    }

    function get_movie() public view returns (Movie memory) {
        return movie;
    }

}
    