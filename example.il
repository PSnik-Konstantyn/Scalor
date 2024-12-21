// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly example
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module example.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{
    .method private hidebysig static void Main(string[] args) cil managed
    {
    .locals (
       [0]  int32 n10     )
   .entrypoint
   //.maxstack  8
   ldloca    n10
   ldc.i4    1
   stind.i4
   ldloca    n10
   ldloc    n10
   ldc.i4    2
   add
   stind.i4
   ldloc    n10
   call void [mscorlib]System.Console::WriteLine(int32)
   ldloca    n10
   call    string [mscorlib]System.Console::ReadLine()
   call int32 [mscorlib]System.Int32::Parse(string)
   stloc n10
   ldloc    n10
   call void [mscorlib]System.Console::WriteLine(int32)
	ret    
}
}