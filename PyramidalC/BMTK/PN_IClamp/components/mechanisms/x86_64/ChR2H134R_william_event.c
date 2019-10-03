/* Created by Language version: 6.2.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
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
 
#define nrn_init _nrn_init__ChR2_william_event
#define _nrn_initial _nrn_initial__ChR2_william_event
#define nrn_cur _nrn_cur__ChR2_william_event
#define _nrn_current _nrn_current__ChR2_william_event
#define nrn_jacob _nrn_jacob__ChR2_william_event
#define nrn_state _nrn_state__ChR2_william_event
#define _net_receive _net_receive__ChR2_william_event 
#define rates rates__ChR2_william_event 
#define states states__ChR2_william_event 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define Irradiance _p[0]
#define gmax _p[1]
#define pulse_width _p[2]
#define light_intensity _p[3]
#define Dt_on _p[4]
#define Dt_off _p[5]
#define nPulses _p[6]
#define gamma _p[7]
#define A _p[8]
#define B _p[9]
#define C _p[10]
#define tauChR2 _p[11]
#define Gd1 _p[12]
#define Gd2 _p[13]
#define Gr _p[14]
#define iopto _p[15]
#define O1 _p[16]
#define O2 _p[17]
#define C1 _p[18]
#define p _p[19]
#define e12 _p[20]
#define e21 _p[21]
#define epsilon1 _p[22]
#define epsilon2 _p[23]
#define F _p[24]
#define S0 _p[25]
#define tally _p[26]
#define DO1 _p[27]
#define DO2 _p[28]
#define DC1 _p[29]
#define Dp _p[30]
#define v _p[31]
#define _g _p[32]
#define _tsav _p[33]
#define _nd_area  *_ppvar[0]._pval
 
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
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static double _hoc_rates();
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(_ho) Object* _ho; { void* create_point_process();
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt();
 static double _hoc_loc_pnt(_vptr) void* _vptr; {double loc_point_process();
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(_vptr) void* _vptr; {double has_loc_point();
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(_vptr)void* _vptr; {
 double get_loc_point_process(); return (get_loc_point_process(_vptr));
}
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata(void* _vptr) { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
   _setdata(_prop);
 }
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 0,0
};
 static Member_func _member_func[] = {
 "loc", _hoc_loc_pnt,
 "has_loc", _hoc_has_loc,
 "get_loc", _hoc_get_loc_pnt,
 "rates", _hoc_rates,
 0, 0
};
 /* declare global and static user variables */
#define EChR2 EChR2_ChR2_william_event
 double EChR2 = 0;
#define Q10_epsilon2 Q10_epsilon2_ChR2_william_event
 double Q10_epsilon2 = 2.77;
#define Q10_epsilon1 Q10_epsilon1_ChR2_william_event
 double Q10_epsilon1 = 1.46;
#define Q10_e21dark Q10_e21dark_ChR2_william_event
 double Q10_e21dark = 1.95;
#define Q10_e12dark Q10_e12dark_ChR2_william_event
 double Q10_e12dark = 1.1;
#define Q10_Gr Q10_Gr_ChR2_william_event
 double Q10_Gr = 2.56;
#define Q10_Gd2 Q10_Gd2_ChR2_william_event
 double Q10_Gd2 = 1.77;
#define Q10_Gd1 Q10_Gd1_ChR2_william_event
 double Q10_Gd1 = 1.97;
#define hc hc_ChR2_william_event
 double hc = 1.98645e-25;
#define sigma_retinal sigma_retinal_ChR2_william_event
 double sigma_retinal = 1.2e-19;
#define temp temp_ChR2_william_event
 double temp = 22;
#define wloss wloss_ChR2_william_event
 double wloss = 1.3;
#define wavelength wavelength_ChR2_william_event
 double wavelength = 470;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "Dt_off", 0, 1e+09,
 "Dt_on", 0, 1e+09,
 "nPulses", 0, 1000,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "EChR2_ChR2_william_event", "mV",
 "temp_ChR2_william_event", "degC",
 "gmax", "uS",
 "pulse_width", "ms",
 "Dt_on", "ms",
 "Dt_off", "ms",
 "nPulses", "1",
 "A", "mV",
 "B", "mV",
 "C", "mV",
 "tauChR2", "ms",
 "Gd1", "1./ms",
 "Gd2", "1./ms",
 "Gr", "1./ms",
 "iopto", "nA",
 0,0
};
 static double C10 = 0;
 static double O20 = 0;
 static double O10 = 0;
 static double delta_t = 0.01;
 static double p0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "EChR2_ChR2_william_event", &EChR2_ChR2_william_event,
 "wavelength_ChR2_william_event", &wavelength_ChR2_william_event,
 "hc_ChR2_william_event", &hc_ChR2_william_event,
 "wloss_ChR2_william_event", &wloss_ChR2_william_event,
 "sigma_retinal_ChR2_william_event", &sigma_retinal_ChR2_william_event,
 "temp_ChR2_william_event", &temp_ChR2_william_event,
 "Q10_Gd1_ChR2_william_event", &Q10_Gd1_ChR2_william_event,
 "Q10_Gd2_ChR2_william_event", &Q10_Gd2_ChR2_william_event,
 "Q10_Gr_ChR2_william_event", &Q10_Gr_ChR2_william_event,
 "Q10_e12dark_ChR2_william_event", &Q10_e12dark_ChR2_william_event,
 "Q10_e21dark_ChR2_william_event", &Q10_e21dark_ChR2_william_event,
 "Q10_epsilon1_ChR2_william_event", &Q10_epsilon1_ChR2_william_event,
 "Q10_epsilon2_ChR2_william_event", &Q10_epsilon2_ChR2_william_event,
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
 static void _hoc_destroy_pnt(_vptr) void* _vptr; {
   destroy_point_process(_vptr);
}
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[3]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "6.2.0",
"ChR2_william_event",
 "Irradiance",
 "gmax",
 "pulse_width",
 "light_intensity",
 "Dt_on",
 "Dt_off",
 "nPulses",
 "gamma",
 "A",
 "B",
 "C",
 "tauChR2",
 "Gd1",
 "Gd2",
 "Gr",
 0,
 "iopto",
 0,
 "O1",
 "O2",
 "C1",
 "p",
 0,
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
  if (nrn_point_prop_) {
	_prop->_alloc_seq = nrn_point_prop_->_alloc_seq;
	_p = nrn_point_prop_->param;
	_ppvar = nrn_point_prop_->dparam;
 }else{
 	_p = nrn_prop_data_alloc(_mechtype, 34, _prop);
 	/*initialize range parameters*/
 	Irradiance = 0;
 	gmax = 0.4;
 	pulse_width = 100;
 	light_intensity = 5;
 	Dt_on = 100;
 	Dt_off = 50;
 	nPulses = 1;
 	gamma = 0.1;
 	A = 10.6408;
 	B = -14.6408;
 	C = -42.7671;
 	tauChR2 = 1.3;
 	Gd1 = 0.117;
 	Gd2 = 0.05;
 	Gr = 0.00019;
  }
 	_prop->param = _p;
 	_prop->param_size = 34;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 
#define _tqitem &(_ppvar[2]._pvoid)
 static void _net_receive(Point_process*, double*, double);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _ChR2H134R_william_event_reg() {
	int _vectorized = 1;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 1,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
  hoc_register_prop_size(_mechtype, 34, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "netsend");
  hoc_register_dparam_semantics(_mechtype, 3, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ChR2_william_event /home/mizzou/Desktop/BLA_SingleCells-master/Pyramidal/BMTK/PN_IClamp/components/mechanisms/x86_64/ChR2H134R_william_event.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(_threadargsprotocomma_ double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[4], _dlist1[4];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   rates ( _threadargscomma_ v ) ;
   DO1 = - ( Gd1 + e12 ) * O1 + e21 * O2 + epsilon1 * F * p * C1 ;
   DO2 = - ( Gd2 + e21 ) * O2 + e12 * O1 + epsilon2 * F * p * ( 1. - C1 - O1 - O2 ) ;
   DC1 = - epsilon1 * F * p * C1 + Gd1 * O1 + Gr * ( 1. - C1 - O1 - O2 ) ;
   Dp = ( S0 - p ) / tauChR2 ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 rates ( _threadargscomma_ v ) ;
 DO1 = DO1  / (1. - dt*( ( - ( Gd1 + e12 ) )*( 1.0 ) )) ;
 DO2 = DO2  / (1. - dt*( ( - ( Gd2 + e21 ) )*( 1.0 ) + ( epsilon2 * F * p )*( ( ( - 1.0 ) ) ) )) ;
 DC1 = DC1  / (1. - dt*( ( - epsilon1 * F * p )*( 1.0 ) + ( Gr )*( ( ( - 1.0 ) ) ) )) ;
 Dp = Dp  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tauChR2 )) ;
 return 0;
}
 /*END CVODE*/
 static int states (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) { {
   rates ( _threadargscomma_ v ) ;
    O1 = O1 + (1. - exp(dt*(( - ( Gd1 + e12 ) )*( 1.0 ))))*(- ( ( e21 )*( O2 ) + ( ( ( epsilon1 )*( F ) )*( p ) )*( C1 ) ) / ( ( - ( Gd1 + e12 ) )*( 1.0 ) ) - O1) ;
    O2 = O2 + (1. - exp(dt*(( - ( Gd2 + e21 ) )*( 1.0 ) + ( epsilon2 * F * p )*( ( ( - 1.0 ) ) ))))*(- ( ( e12 )*( O1 ) + ( ( ( epsilon2 )*( F ) )*( p ) )*( ( 1. - C1 - O1 ) ) ) / ( ( - ( Gd2 + e21 ) )*( 1.0 ) + ( ( ( epsilon2 )*( F ) )*( p ) )*( ( ( - 1.0 ) ) ) ) - O2) ;
    C1 = C1 + (1. - exp(dt*(( - epsilon1 * F * p )*( 1.0 ) + ( Gr )*( ( ( - 1.0 ) ) ))))*(- ( ( Gd1 )*( O1 ) + ( Gr )*( ( 1. - O1 - O2 ) ) ) / ( ( ( ( - epsilon1 )*( F ) )*( p ) )*( 1.0 ) + ( Gr )*( ( ( - 1.0 ) ) ) ) - C1) ;
    p = p + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tauChR2)))*(- ( ( ( S0 ) ) / tauChR2 ) / ( ( ( ( - 1.0 ) ) ) / tauChR2 ) - p) ;
   }
  return 0;
}
 
static int  rates ( _threadargsprotocomma_ double _lv ) {
   double _le12dark , _le21dark , _llogphi0 , _lEphoton , _lflux ;
 _le12dark = 0.011 ;
   _le21dark = 0.008 ;
   epsilon1 = 0.8535 ;
   epsilon2 = 0.14 ;
   if ( Irradiance > 0.0 ) {
     _llogphi0 = log ( 1. + Irradiance / 0.024 ) ;
     }
   else {
     _llogphi0 = 0. ;
     }
   e12 = _le12dark + 0.005 * _llogphi0 ;
   e21 = _le21dark + 0.004 * _llogphi0 ;
   S0 = 0.5 * ( 1. + tanh ( 120. * ( 100. * Irradiance - 0.1 ) ) ) ;
   _lEphoton = 1.E9 * hc / wavelength ;
   _lflux = 1000. * Irradiance / _lEphoton ;
   F = _lflux * sigma_retinal / ( wloss * 1000. ) ;
    return 0; }
 
static double _hoc_rates(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r = 1.;
 rates ( _p, _ppvar, _thread, _nt, *getarg(1) );
 return(_r);
}
 
static void _net_receive (_pnt, _args, _lflag) Point_process* _pnt; double* _args; double _lflag; 
{  double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _thread = (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;   _p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
  if (_tsav > t){ extern char* hoc_object_name(); hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t;   if (_lflag == 1. ) {*(_tqitem) = 0;}
 {
   if ( _lflag  == 0.0 ) {
     if ( Irradiance  == 0.0 ) {
       Irradiance = light_intensity ;
       net_send ( _tqitem, _args, _pnt, t +  Dt_on , 1.0 ) ;
       }
     }
   else {
     Irradiance = 0.0 ;
     _lflag = 0.0 ;
     }
   } }
 
static int _ode_count(int _type){ return 4;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 (_p, _ppvar, _thread, _nt);
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 4; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  C1 = C10;
  O2 = O20;
  O1 = O10;
  p = p0;
 {
   rates ( _threadargscomma_ v ) ;
   C1 = 1. ;
   O1 = 0. ;
   O2 = 0. ;
   p = 0. ;
   }
 
}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _tsav = -1e20;
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
 initmodel(_p, _ppvar, _thread, _nt);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   iopto = ( gmax * ( A + B * exp ( v / C ) ) / v * ( O1 + gamma * O2 ) * ( v - EChR2 ) ) ;
   }
 _current += iopto;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
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
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
 	}
 _g = (_g - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
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
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
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
 {   states(_p, _ppvar, _thread, _nt);
  }}}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(O1) - _p;  _dlist1[0] = &(DO1) - _p;
 _slist1[1] = &(O2) - _p;  _dlist1[1] = &(DO2) - _p;
 _slist1[2] = &(C1) - _p;  _dlist1[2] = &(DC1) - _p;
 _slist1[3] = &(p) - _p;  _dlist1[3] = &(Dp) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif
