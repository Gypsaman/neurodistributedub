
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct Product {
        
        string name;
        uint256 price;
        uint256 quantity;
    }

    Product public product;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(string memory _name, uint256  _price, uint256 _quantity) {
        
        product.name = _name;
        product.price = _price;
        product.quantity = _quantity;


        owner = msg.sender;

    }
    function update_quantity(uint256 _quantity) public onlyOwner {
        product.quantity = _quantity;
    }

    function get_product() public view returns (Product memory) {
        return product;
    }

}
    