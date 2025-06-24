# no compatible reference error

It's a common error while running `HLA-LA.pl`.

The error message is at **Line 364** of `HLA-LA.pl`:

```text
Have found no compatible reference specifications in /work/clwu/miniconda3/envs/hla-la-env/opt/hla-la/src/../graphs/PRG_MHC_GRCh38_withIMGT/knownReferences - create a file for this BAM file and try again. at /work/clwu/miniconda3/envs/hla-la-env/bin/HLA-LA.pl line 364.
```

## Why do we encounter this error?

There could be two main reasons to encounter this error:

1. The `additionalReferences` is not at the right place. So `HLA-LA.pl` cannot find it. -> We need to ensure the `additionalReferences` at the right place.
2. The BAM is a particular version, that not existing reference match to it. For example, the BAM remapped by [[hla-mapper]]. -> We need to create a corresponding reference and add it to the env.

Normally, if the additionalReferences are in the right place and the BAM is in a general version, the reference should be identified right after running HLA-LA without error messages.

I have an experience that the BAM is from `hla-mapper`, so no existing reference match to it. To solve it, we need to have the right reference. See steps [below](#steps-to-prepare-the-reference).

## Place `additionalReferences /PRG_MHC_GRCh38_withIMGT` at the right place

While running the `HLA-LA.pl`, it search two places for the references:

1. **knownReferences**
2. **additionalReferences**

Known references in `hla-la-env` is in `graphic`: `/work/clwu/miniconda3/envs/hla-la-env/opt/hla-la/graphs/PRG_MHC_GRCh38_withIMGT/knownReferences`.
There are only 4 files:

- 1000G_B37_noChr.txt 
- B37_generic_noChr.txt
- 1000G_B38.txt
- PRG_MHC_GRCh38_withIMGT.txt

Additional references in `hla-la-env` should be in `src`: `/work/clwu/miniconda3/envs/hla-la-env/opt/hla-la/src/additionalReferences/PRG_MHC_GRCh38_withIMGT`.

If no `additionalReferences` presenced, they could be downloaded from the GitHub (`additionalReferences /PRG_MHC_GRCh38_withIMGT`) and be placed under the hla-la-env (see the path from the error message).

If we create our own reference, we put it in the `additionalReference`.

## Steps to prepare the reference

(TODO)
