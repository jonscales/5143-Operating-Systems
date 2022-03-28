## Reader Writer Part 1

#### Due: TBD

Using the python concurrency mechanism that best fits the job, implement a reader / writer framework that will keep a shared memory section safe so that readers will get accurate data and writers won't conflict with each other. This is the first part of our concurrency project in which we protect a critical section of local code. Next project will involve protecting a similar critical section of code via network requests.

The reader/writer problem is a classic which is still very much relevant in todays architexture, especially with database and file servers being so prevalent. The problem is as follows:

> -   Any processes can read from the shared resource, even while others are reading.
> -   Any process may write to the shared resource.
> -   No process may access the shared resource for either reading or writing <ins>**while another process is in the act of writing to it**</ins>.
>
>     <sub>Note: The term "process" is interchangeable with "thread".</sub>

This project is not very hard, so don't overthink it. We will expand on this project for our next one, adding the ability to synchronize events over the network. For now, we are only locking the "shared memory" to ensure data integrity.

### Reader

-   Wants to read from shared memory.
-   Makes no changes.

### Writer

-   Wants to edit one or more shared memory values.
-   Needs to obtain access before this happens.
-   The writer will execute a small set of instructions and then write the result to shared memory.

## Example

An example `readerWriter` implementation can be found [here](readerWriter.py) in this folder. This is a basic example, and it actually works. The issue is that its shared memory is a single global variable making it not to hard to manage.

One issue this example does not show is that there needs to be multiple instances of readers and writers. In fact, there should be at least a 5 to 1 reader to writer ratio.

-   Your program should specify with command line params how many writers should be created.
-   Each writer will execute randomly generated instructions that will ultimately change shared memory.
-   I would make it so no instruction uses values over 9, keeping

### Instructions

The type of instructions that will be executed are listed below:

```
['MOV','ADD','SUB','MUL','DIV','SET','READ','WRITE']
```

A list of examples where R1 and R2 are registers. There can be more than 2 registers, but that is not really a factor for this program. It will be relevant next program.

-   'MOV': `MOV R1 R2` Copy value from register `R1` to register `R2`
-   'ADD': `ADD R1 R2` Add values in `R1` and `R2`, storing result in `R1`.
-   'SUB': `SUB R1 R2` Subtract values in `R1` and `R2`, storing result in `R1`.
-   'MUL': `MUL R1 R2` Multiply values in `R1` and `R2`, storing result in `R1`.
-   'DIV': `DIV R1 R2` Divide values in `R1` and `R2`, storing result in `R1`.
-   'SET': `SET R2 7` Load 7 into `R2`.
-   'READ': `READ R2 A100` Read memory location `A100` into `R2`.
-   'WRITE': `WRITE R1 B100` Write contents of A into memory location `B100`.

### Generate instructions

Generate a list of over `N` instructions (minimum in the hundreds) using the guidelines above, giving regards to our memory contraints below. This means:

-   Each file should generate instructions depending on whether it is a reader or a writer.
-   Have the ability to generate instructions that only read or write to 1 section of memory (A,B,C) but the default should be reading and writing to all of the three sections.
-   Readers only `READ` memory locations.
-   Writers have to `READ` memory locations in order to execute instructions. Below is a basic instruction:

```
READ A205 R1
READ B240 R2
ADD R1 R2
WRITE R1 A205
```

or

```python
def randInstruction():

    choices = ["ADD", "SUB", "MUL", "DIV"]
    registers = ["R1", "R2"]
    memblocks = ["A", "B", "C"]
    memaddress = [x for x in range(100, 255, 5)]

    shuffle(choices)
    shuffle(registers)
    shuffle(memblocks)
    shuffle(memaddress)

    itype = choices[0]
    r1, r2 = registers[:2]
    mb1, mb2 = memblocks[:2]
    madd1, madd2 = memaddress[:2]

    inst = ""
    inst += f"READ {mb1}{madd1} {r1}\n"
    inst += f"READ {mb2}{madd2} {r2}\n"
    inst += f"{itype} {r1} {r2}\n"
    inst += f"WRITE {r1} {mb1}{madd1}\n"
    return inst
```

Output:

```
READ B110 R1
READ A170 R2
ADD R1 R2
WRITE R1 B110

READ A185 R1
READ C210 R2
DIV R1 R2
WRITE R1 A185

READ C205 R1
READ A155 R2
SUB R1 R2
WRITE R1 C205
```

#### memory.json

```python
{
    "A": {
        "100": null,
        "105": null,
        ...
        "130": null,
        ...
        "245": null,
        "250": null
    },
    "B": {
        "100": null,
        "105": null,
        ...
        "125": null,
        ...
        "245": null,
        "250": null
    },
    "C": {
        "100": null,
        "105": null,
        "110": null,
        ...
        "245": null,
        "250": null
    }
}
```

### Shared Memory

-   There are three components: A, B, C with addresses from 100-250 inclusive.
-   When implementing your locking mechanisms to this shared memory space, you can initially assume that the entire space (A,B,C) can all be locked at once.
-   But, some implementations will need to lock (A) (B) and (C) seperately.
-   When your program begins load `memory.json` to "load" the memory.
-   When your program finishes write your memory back to `memory.json`.

### Experiment

-   Assume `W` writers, where: `1 < W < 20`.
-   Assume `R` = `5 * W`
-   Generate `N` files of `m` random instructions, where `N = R * W` and `m > 100`.
-   Remember you need to have ability to generate instructions that stay within a single memory block!
-   You need to time the running of all the instructions under two conditions:
    -   The lock locks all of the memory blocks (A,B,C)
    -   The lock only locks the necessary component (A), (B), (C) as needed. This does mean we might need to obtain more than one lock per instruction!
-   What issues will we encounter?
-   Can we make any improvements.
-   Can we obtain speedup by limiting instructions to only accessing one memory block?

### References + Help

-   https://realpython.com/intro-to-python-threading/
-   https://realpython.com/python-concurrency/
-   https://realpython.com/async-io-python/
-   https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work/51116910#51116910

#### More:

-   https://medium.com/geekculture/distributed-lock-implementation-with-redis-and-python-22ae932e10ee
-   https://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/