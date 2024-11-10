//SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

import {Test,console} from 'forge-std/Test.sol';
import '../src/Books.sol';

contract TestBooks_Master is Test {
    Books books;

    function setUp() public {
        books = new Books("Programming Foundry", "Cesar Garcia", 100);
    }

    function test_Master_update_pages() public {
        books.update_pages(200);
        assertEq(books.get_book().pages, 200);
    }

    function test_Master_get_book() public view {
        Books.Book memory book = books.get_book();
        assertEq(book.title, "Programming Foundry");

        assertEq(book.pages, 120);
    }

}