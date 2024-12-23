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
       [0]  float32 x     )
   .entrypoint
   //.maxstack  8
   ldloca    x
   ldc.r4    1.0
   neg
   stind.r4
   ldloca    x
   ldloc    x
   ldc.r4    2.0
   add
   stind.r4
   ldloc    x
   call void [mscorlib]System.Console::WriteLine(float32)
   call    string [mscorlib]System.Console::ReadLine()
   call float32 [mscorlib]System.Single::Parse(string)
   stloc x
   ldloc    x
   call void [mscorlib]System.Console::WriteLine(float32)
   ldloc    x
   ldc.i4    2
   conv.r4
   ceq
   brfalse    m1
   ldloc    x
   call void [mscorlib]System.Console::WriteLine(float32)
   br    m2
m1:
   ldloca    x
   ldloc    x
   ldc.r4    8.0
   add
   stind.r4
   ldloc    x
   call void [mscorlib]System.Console::WriteLine(float32)
m2:
m3:
   ldloc    x
   ldc.i4    3
   conv.r4
   cgt
   brfalse    m4
   ldloc    x
   call void [mscorlib]System.Console::WriteLine(float32)
   ldloca    x
   ldloc    x
   ldc.r4    1.0
   sub
   stind.r4
   br    m3
m4:
	ret    
}
}