#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _izh_reg(void);
extern void _pyr2pyr_reg(void);
extern void _synapse_inter2pyr_reg(void);
extern void _vecevent_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," izh.mod");
    fprintf(stderr," pyr2pyr.mod");
    fprintf(stderr," synapse_inter2pyr.mod");
    fprintf(stderr," vecevent.mod");
    fprintf(stderr, "\n");
  }
  _izh_reg();
  _pyr2pyr_reg();
  _synapse_inter2pyr_reg();
  _vecevent_reg();
}
