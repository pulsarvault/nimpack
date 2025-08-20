// Rohit: Recursion, Factorial, Memoization

function factorial(n: number): number {
  if (n < 0) throw new Error('No factorial for negatives!');
  if (n === 0) return 1;
  return n * factorial(n - 1);
}

console.log(factorial(5); 
