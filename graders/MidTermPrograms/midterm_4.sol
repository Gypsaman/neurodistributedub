
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct Book {
        
        string title;
        string author;
        uint256 pages;
    }

    Book public book;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(string memory _title, string memory _author, uint256 _pages) {
        
        book.title = _title;
        book.author = _author;
        book.pages = _pages;


        owner = msg.sender;

    }
    function update_pages(uint256 _pages) public onlyOwner {
        book.pages = _pages;
    }

    function get_book() public view returns (Book memory) {
        return book;
    }

}
    