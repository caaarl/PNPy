#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _AXNODE_reg(void);
extern void _AXFLUT_reg(void);
extern void _vecevent_reg(void);
extern void _xtra_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," AXNODE.mod");
    fprintf(stderr," AXFLUT.mod");
    fprintf(stderr," vecevent.mod");
    fprintf(stderr," xtra.mod");
    fprintf(stderr, "\n");
  }
  _AXNODE_reg();
  _AXFLUT_reg();
  _vecevent_reg();
  _xtra_reg();
}
