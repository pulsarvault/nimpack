interface Person {
    name: string;
    age: number;
}

type UserID = string;

function greet(userId: UserID, person: Person): void {
    console.log("Hello " + person.name + " (ID: " + userId + ")");
}

let age: number = 25;
let isActive: boolean = true;
