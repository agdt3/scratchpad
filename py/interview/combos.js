#! /bin/node

var input = [14, 85, 8, 2, 1, 3, 14, 6, 19, 1];
var input2 = [14, 6, 4, 8, 25, 17, 39];
console.log(input);
var expected = [1, 1, 2, 3, 6, 8, 14, 14, 19, 85];

// no tail recursion
function mergesort(arr) {
  if (arr.length === 0 || arr.length === 1) {
    return arr;
  }
  else {
    var len = arr.length;
    var half = Math.floor(len/2);
    var left = mergesort(arr.slice(0, half));
    var right = mergesort(arr.slice(half, len));
    return merge(left, right);
  }
}

function merge(left, right) {
  var result = [];
  var leng = Math.min(left.length, right.length);
  // Internal ordering established so remainder will
  // always be internally ordered from least to greatest
  while (left.length > 0 && right.length > 0) {
    var lt_len = left.length;
    var rt_len = right.length;
    if (left[0] < right[0]) {
      result.push(left.shift());
    }
    else {
      result.push(right.shift());
    }
  }

  // Push leftovers, if any, onto the result stack
  while (left.length > 0) {
    result.push(left.shift());
  }

  while (right.length > 0) {
    result.push(right.shift());
  }

  return result;
}


var res = mergesort(input);
console.log(res);

function quicksort(arr) {
  if (arr.length === 0 || arr.length === 1) {
    return arr;
  }
  else {
    var pivot = arr[0];
    var middle = [];
    var lesser = [];
    var greater = [];
    for (var i = 0; i < arr.length; i++) {
      if (arr[i] < pivot) {
        lesser.push(arr[i]);
      }
      else if (arr[i] > pivot) {
        greater.push(arr[i]);
      }
      else {
        middle.push(arr[i]);
      }
    }
    return quicksort(lesser).concat(middle).concat(quicksort(greater));
  }
}

var res = quicksort(input);
console.log(res);

var elements = ['a', 'b', 'c', 'd'];
function powerset(elements) {
  for (var i = 0; i < elements.length; i++) {
    var el = elements[i];
    for (var j = i; j < elements.length; j++) {
      var new_el = make_new_element(el, elements[j]);
      if (new_el && !elements.includes(new_el)) {
        elements.push(new_el);
      }
    }
  }
  return elements;
}

function make_new_element(el1, el2) {
  for (var i = 0; i < el1.length; i++) {
    if (el2.includes(el1[i])) {
      return false;
    }
  }

  return (el1 + el2).split('').sort().join('');
}

var res = powerset(elements);
console.log(res);

class Tree {
  constructor(value, left, right, par) {
    this.value = value || null;
    this.left = left || null;
    this.right = right || null;
    this.par = par || null;
  }

  insert(value) {
    if (this.value === null) {
      this.value = value;
    }
    else if (value < this.value) {
      if (this.left !== null) {
        this.left.insert(value);
      }
      else {
        var left = new Tree(value, null, null);
        this.left = left;
      }
    }
    else if (value > this.value) {
      if (this.right !== null) {
        this.right.insert(value);
      }
      else {
        var right = new Tree(value, null, null);
        this.right = right;
      }
    }
  }

  remove(value) {
    var node = this.search(value);
    if (node === null) {
      return;
    }
    else {
      if (node.left === null && node.right === null) {
         
      }
    }
  }

  list() {
    var array = [];
    this.inorder((x) => {array.push(x.value)});
    return array;
  }

  search(value) {
    if (this.value === value) {
      return this;
    }
    else if (value < this.value) {
      return this.left._search(value);
    }
    else if (value > this.value) {
      return this.right._search(value);
    }
    else {
      return null;
    }
  }

  inorder(func) {
    if (this.left) {
      this.left.inorder(func);
    }
    func(this);
    if (this.right) {
      this.right.inorder(func);
    }
  }

  reverse_inorder(func) {
   if (this.right) {
      this.right.reverse_inorder();
    }
    func(this);
    if (this.left) {
      this.left.reverse_inorder();
    }
  }

  preorder(func) {
    func(this);
    if (this.left) {
      this.left.preorder();
    }
    if (this.right) {
      this.right.preorder();
    }
  }

  postorder(func) {
    if (this.left) {
      this.left.postorder();
    }
    if (this.right) {
      this.right.postorder();
    }
    func(this);
  }
}

function build_tree(elements) {
  var tree = new Tree();
  elements.forEach((element) => {
    tree.insert(element);
  });
  return tree;
}

var tree = build_tree(input2);
//console.log(tree);
//tree.inorder();
//tree.preorder();
//tree.postorder();
//tree.reverse_inorder();
var test = tree.list();
console.log(test);

class Heap {
  constructor(elements) {
    this._elements = [];
    this._create(elements);
  }

  _create(elements) {
   elements.forEach(element => {
    this.insert(element);
   });
  }

  insert(element) {
    if (this._elements.length === 0) {
      this._elements[0] = element;
    }
    else {
      var index = 0;
      while (true) {
        /*
        if (index >= this._elements.length) {
          this._elements.push(element);
          break;
        }
        */

        console.log(index);
        if (element < this._elements[index]) {
          index = 2 * index + 1;
        }
        else if (element > this._elements[index]) {
          index = 2 * index + 2;
        }
        else if (this._elements[index] === undefined) {
          this._elements.push(element);
          break;
        }
      }
    }
  }
}

var heap = new Heap(input);
console.log(heap);

/*
function create_heap(elements) {
  elemenets.forEach
}
*/
