/* Created by Language version: 6.2.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__ncaBC
#define _nrn_initial _nrn_initial__ncaBC
#define nrn_cur _nrn_cur__ncaBC
#define _nrn_current _nrn_current__ncaBC
#define nrn_jacob _nrn_jacob__ncaBC
#define nrn_state _nrn_state__ncaBC
#define _net_receive _net_receive__ncaBC 
#define _f_trates _f_trates__ncaBC 
#define rates rates__ncaBC 
#define states states__ncaBC 
#define trates trates__ncaBC 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gncabar _p[0]
#define gnca _p[1]
#define inca _p[2]
#define cinf _p[3]
#define dinf _p[4]
#define ctau _p[5]
#define dtau _p[6]
#define c _p[7]
#define d _p[8]
#define Dc _p[9]
#define Dd _p[10]
#define enca _p[11]
#define cexp _p[12]
#define dexp _p[13]
#define _g _p[14]
#define _ion_enca	*_ppvar[0]._pval
#define _ion_inca	*_ppvar[1]._pval
#define _ion_dincadv	*_ppvar[2]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_rates(void);
 static void _hoc_states(void);
 static void _hoc_trates(void);
 static void _hoc_vtrap(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_ncaBC", _hoc_setdata,
 "rates_ncaBC", _hoc_rates,
 "states_ncaBC", _hoc_states,
 "trates_ncaBC", _hoc_trates,
 "vtrap_ncaBC", _hoc_vtrap,
 0, 0
};
#define vtrap vtrap_ncaBC
 extern double vtrap( double , double );
 /* declare global and static user variables */
#define usetable usetable_ncaBC
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "usetable_ncaBC", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gncabar_ncaBC", "mho/cm2",
 "gnca_ncaBC", "mho/cm2",
 "inca_ncaBC", "mA/cm2",
 "ctau_ncaBC", "ms",
 "dtau_ncaBC", "ms",
 0,0
};
 static double c0 = 0;
 static double delta_t = 1;
 static double d0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "usetable_ncaBC", &usetable_ncaBC,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "6.2.0",
"ncaBC",
 "gncabar_ncaBC",
 0,
 "gnca_ncaBC",
 "inca_ncaBC",
 "cinf_ncaBC",
 "dinf_ncaBC",
 "ctau_ncaBC",
 "dtau_ncaBC",
 0,
 "c_ncaBC",
 "d_ncaBC",
 0,
 0};
 static Symbol* _nca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 15, _prop);
 	/*initialize range parameters*/
 	gncabar = 0;
 	_prop->param = _p;
 	_prop->param_size = 15;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_nca_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* enca */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* inca */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dincadv */
 
}
 static void _initlists();
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _nca_BC_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("nca", 2.0);
 	_nca_sym = hoc_lookup("nca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
  hoc_register_prop_size(_mechtype, 15, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "nca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "nca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "nca_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ncaBC /home/mizzou/Desktop/backup/BLA_SingleCells-master/CA3_Tyler/BMTK/PN_IClamp/components/mechanisms/x86_64/nca_BC.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96520.0;
 static double R = 8.3134;
 static double _zq10 ;
 static double *_t_cinf;
 static double *_t_cexp;
 static double *_t_dinf;
 static double *_t_dexp;
 static double *_t_ctau;
 static double *_t_dtau;
static int _reset;
static char *modelname = "nca.mod  ";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int _f_trates(double);
static int rates(double);
static int states();
static int trates(double);
 static void _n_trates(double);
 
static int  states (  ) {
   trates ( _threadargscomma_ v ) ;
   c = c + cexp * ( cinf - c ) ;
   d = d + dexp * ( dinf - d ) ;
   
/*VERBATIM*/
        return 0;
  return 0; }
 
static void _hoc_states(void) {
  double _r;
   _r = 1.;
 states (  );
 hoc_retpushx(_r);
}
 
static int  rates (  double _lv ) {
   double _lalpha , _lbeta , _lsum ;
 _zq10 = pow( 3.0 , ( ( celsius - 6.3 ) / 10.0 ) ) ;
   _lalpha = - 0.19 * vtrap ( _threadargscomma_ _lv - 19.88 , - 10.0 ) ;
   _lbeta = 0.046 * exp ( - _lv / 20.73 ) ;
   _lsum = _lalpha + _lbeta ;
   ctau = 1.0 / _lsum ;
   cinf = _lalpha / _lsum ;
   _lalpha = 0.00016 / exp ( - _lv / 48.4 ) ;
   _lbeta = 1.0 / ( exp ( ( - _lv + 39.0 ) / 10.0 ) + 1.0 ) ;
   _lsum = _lalpha + _lbeta ;
   dtau = 1.0 / _lsum ;
   dinf = _lalpha / _lsum ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   _r = 1.;
 rates (  *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_trates, _tmin_trates;
 static void _check_trates();
 static void _check_trates() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_dt;
  static double _sav_celsius;
  if (!usetable) {return;}
  if (_sav_dt != dt) { _maktable = 1;}
  if (_sav_celsius != celsius) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_trates =  - 100.0 ;
   _tmax =  100.0 ;
   _dx = (_tmax - _tmin_trates)/200.; _mfac_trates = 1./_dx;
   for (_i=0, _x=_tmin_trates; _i < 201; _x += _dx, _i++) {
    _f_trates(_x);
    _t_cinf[_i] = cinf;
    _t_cexp[_i] = cexp;
    _t_dinf[_i] = dinf;
    _t_dexp[_i] = dexp;
    _t_ctau[_i] = ctau;
    _t_dtau[_i] = dtau;
   }
   _sav_dt = dt;
   _sav_celsius = celsius;
  }
 }

 static int trates(double _lv){ _check_trates();
 _n_trates(_lv);
 return 0;
 }

 static void _n_trates(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 _f_trates(_lv); return; 
}
 _xi = _mfac_trates * (_lv - _tmin_trates);
 if (isnan(_xi)) {
  cinf = _xi;
  cexp = _xi;
  dinf = _xi;
  dexp = _xi;
  ctau = _xi;
  dtau = _xi;
  return;
 }
 if (_xi <= 0.) {
 cinf = _t_cinf[0];
 cexp = _t_cexp[0];
 dinf = _t_dinf[0];
 dexp = _t_dexp[0];
 ctau = _t_ctau[0];
 dtau = _t_dtau[0];
 return; }
 if (_xi >= 200.) {
 cinf = _t_cinf[200];
 cexp = _t_cexp[200];
 dinf = _t_dinf[200];
 dexp = _t_dexp[200];
 ctau = _t_ctau[200];
 dtau = _t_dtau[200];
 return; }
 _i = (int) _xi;
 _theta = _xi - (double)_i;
 cinf = _t_cinf[_i] + _theta*(_t_cinf[_i+1] - _t_cinf[_i]);
 cexp = _t_cexp[_i] + _theta*(_t_cexp[_i+1] - _t_cexp[_i]);
 dinf = _t_dinf[_i] + _theta*(_t_dinf[_i+1] - _t_dinf[_i]);
 dexp = _t_dexp[_i] + _theta*(_t_dexp[_i+1] - _t_dexp[_i]);
 ctau = _t_ctau[_i] + _theta*(_t_ctau[_i+1] - _t_ctau[_i]);
 dtau = _t_dtau[_i] + _theta*(_t_dtau[_i+1] - _t_dtau[_i]);
 }

 
static int  _f_trates (  double _lv ) {
   double _ltinc ;
 rates ( _threadargscomma_ _lv ) ;
   _ltinc = - dt * _zq10 ;
   cexp = 1.0 - exp ( _ltinc / ctau ) ;
   dexp = 1.0 - exp ( _ltinc / dtau ) ;
    return 0; }
 
static void _hoc_trates(void) {
  double _r;
    _r = 1.;
 trates (  *getarg(1) );
 hoc_retpushx(_r);
}
 
double vtrap (  double _lx , double _ly ) {
   double _lvtrap;
 if ( fabs ( _lx / _ly ) < 1e-6 ) {
     _lvtrap = _ly * ( 1.0 - _lx / _ly / 2.0 ) ;
     }
   else {
     _lvtrap = _lx / ( exp ( _lx / _ly ) - 1.0 ) ;
     }
   
return _lvtrap;
 }
 
static void _hoc_vtrap(void) {
  double _r;
   _r =  vtrap (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ hoc_execerror("ncaBC", "cannot be used with CVODE"); return 0;}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_nca_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_nca_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_nca_sym, _ppvar, 2, 4);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  c = c0;
  d = d0;
 {
   trates ( _threadargscomma_ v ) ;
   c = cinf ;
   d = dinf ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  enca = _ion_enca;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   gnca = gncabar * c * c * d ;
   inca = gnca * ( v - enca ) ;
   }
 _current += inca;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  enca = _ion_enca;
 _g = _nrn_current(_v + .001);
 	{ double _dinca;
  _dinca = inca;
 _rhs = _nrn_current(_v);
  _ion_dincadv += (_dinca - inca)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_inca += inca ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  enca = _ion_enca;
 { error =  states();
 if(error){fprintf(stderr,"at line 53 in file nca_BC.mod:\n	SOLVE states\n"); nrn_complain(_p); abort_run(error);}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
   _t_cinf = makevector(201*sizeof(double));
   _t_cexp = makevector(201*sizeof(double));
   _t_dinf = makevector(201*sizeof(double));
   _t_dexp = makevector(201*sizeof(double));
   _t_ctau = makevector(201*sizeof(double));
   _t_dtau = makevector(201*sizeof(double));
_first = 0;
}
