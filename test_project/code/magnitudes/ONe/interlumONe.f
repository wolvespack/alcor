      subroutine interlumone(cooling_time,
     &                       wd_mass,
     &                       luminosity,
     &                       ubvri_u,
     &                       ubvri_b,
     &                       ubvri_v,
     &                       ubvri_r,
     &                       ubvri_i,
     &                       ubvri_j,
     &                       effective_temperature,
     &                       surface_gravity_logarithm)
C     This subroutine interpolates luminosity of the DA ONe WD
C     together with Johnson colors (U,B,V,R,I)

      implicit none

C     TODO: find out the meaning of following constants
      integer, parameter :: NCOL = 6,
     &                      NCOL2 = 5,
     &                      NROW = 300
      real, parameter :: SOLAR_MASS_KG = 1.989e30,
     &                   GRAVITATIONAL_CONST_CM_S_KG = 6.67e-5

      integer :: i,
     &           model,
     &           modlog
      real :: wd_mass,
     &        cooling_time,
     &        y,
     &        mv,
     &        mj,
     &        cbv,
     &        cvi,
     &        cvr,
     &        cuv,
     &        zlte,
     &        zlr,
     &        luminosity,
     &        ubvri_u,
     &        ubvri_b,
     &        ubvri_v,
     &        ubvri_r,
     &        ubvri_i,
     &        ubvri_j,
     &        effective_temperature,
     &        surface_gravity_logarithm

      integer :: ndatsone(NCOL),
     &           ndatsone2(NCOL2)
      real :: mtabone(NCOL),
     &        mtabone2(NCOL2),
     &        mvtabone(NCOL,NROW),
     &        ltabone(NCOL,NROW),
     &        lgtabone(NCOL,NROW),
     &        lgtetabone(NCOL,NROW),
     &        bvtabone(NCOL,NROW),
     &        vitabone(NCOL,NROW),
     &        vrtabone(NCOL,NROW),
     &        uvtabone(NCOL,NROW),
     &        jone(NCOL,NROW),
     &        lgrtabone(NCOL2,NROW),
     &        lgt2tabone(NCOL2,NROW),
     &        tprewd1(NCOL),
     &        tprewd2(NCOL2)
 
      common /fredone/ lgtabone, ltabone, mvtabone, lgtetabone
      common /fredone2/ mtabone, ndatsone
      common /colorsone/ bvtabone, vitabone, vrtabone, uvtabone, jone
      common /newone/ lgrtabone, lgt2tabone
      common /newone2/ mtabone2, ndatsone2
      
C     ---   Interpolation  ---
C     TODO: find out the meaning of following variables
      model = 1
      modlog = 0
      y = log10(cooling_time) + 9.0

      do i = 1, NCOL
C       TODO: find out the meaning of tprewd1 and tprewd2
        tprewd1(i) = 0.0
      end do

      do i = 1, NCOL2
        tprewd2(i) = 0.0
      end do

C     TODO: find out what is going on here
      call interp(model,modlog,y,wd_mass,NCOL,ndatsone,lgtabone,tprewd1,
     &     mtabone,ltabone,luminosity)
      call interp(model,modlog,y,wd_mass,NCOL,ndatsone,lgtabone,tprewd1,
     &     mtabone,mvtabone,mv)
      call interp(model,modlog,y,wd_mass,NCOL,ndatsone,lgtabone,tprewd1,
     &     mtabone,bvtabone,cbv)
      call interp(model,modlog,y,wd_mass,NCOL,ndatsone,lgtabone,tprewd1,
     &     mtabone,vitabone,cvi)
      call interp(model,modlog,y,wd_mass,NCOL,ndatsone,lgtabone,tprewd1,
     &     mtabone,vrtabone,cvr)
      call interp(model,modlog,y,wd_mass,NCOL,ndatsone,lgtabone,tprewd1,
     &     mtabone,uvtabone,cuv)
      call interp(model,modlog,y,wd_mass,NCOL,ndatsone,lgtabone,tprewd1,
     &     mtabone,lgtetabone,zlte)
      call interp(model,modlog,y,wd_mass,NCOL2,ndatsone2,lgt2tabone,
     &     tprewd2,mtabone2,lgrtabone,zlr)
      call interp(model,modlog,y,wd_mass,NCOL,ndatsone,lgtabone,tprewd1,
     &     mtabone,jone,mj)

      effective_temperature = 10.0 ** zlte

C     TODO: find out the meaning of 6.696e10 constant
      surface_gravity_logarithm = log10(GRAVITATIONAL_CONST_CM_S_KG) 
     &                            + log10(wd_mass * SOLAR_MASS_KG) 
     &                            - 2.0 * (zlr + log10(6.696e10))
      ubvri_u = cuv + mv
      ubvri_b = cbv + mv
      ubvri_v = mv
      ubvri_r = mv - cvr
      ubvri_i = mv - cvi
      ubvri_j = mj

      end subroutine
