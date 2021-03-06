      subroutine intermag(mass,
     &                    lumi,
     &                    numberOfMassesWithColors,
     &                    ntrk,
     &                    mtrk,
     &                    luminosity,
     &                    color_U,
     &                    color_B,
     &                    color_V,
     &                    color_R,
     &                    color_I,
     &                    color_J,
     &                    c1,
     &                    c2,
     &                    c3,
     &                    c4,
     &                    c5,
     &                    c6)
C     Interpolating luminosity of a DA WD according to its mass and 
C     cooling time using the cooling sequence from input (corresponding 
C     to certain metallicity)
C       TODO: find out what is the difference b/n lumi and luminosity
C       lumi: luminosity
C       TODO: find out what is the difference b/n color_U and c1, etc..
C       c1,c2,c3,c4,c5: Johnson colors
      implicit none

      integer :: numberOfMassesWithColors,
     &           i,
     &           k,
     &           check1,
     &           check2,
     &           check3,
     &           i1,
     &           i2,
     &           ntrk(numberOfMassesWithColors),
     &           ns1,
     &           ns2
      real :: mass,
     &        lumi,
     &        c1,
     &        c2,
     &        c3,
     &        c4,
     &        c5,
     &        c6,
     &        c_1,
     &        c_2,
     &        a1,
     &        a2,
     &        b1,
     &        b2,
     &        mtrk(numberOfMassesWithColors),
     &        luminosity(numberOfMassesWithColors,*),
     &        color_U(numberOfMassesWithColors,*),
     &        color_B(numberOfMassesWithColors,*),
     &        color_V(numberOfMassesWithColors,*),
     &        color_R(numberOfMassesWithColors,*),
     &        color_I(numberOfMassesWithColors,*),
     &        color_J(numberOfMassesWithColors,*)

C     TODO: find out the meaning of check variables
      check1 = 0
      check2 = 0
      check3 = 0

C     TODO: get rid of all todo
C     TODO: find a way to split this
C     Smaller mass than known -> linear 2D extrapolation (using 
C     luminosity and mass)
      if (mass <= mtrk(1)) then
C       TODO: find out the meaning of ns1, ns2, ntrk variables
        ns1 = ntrk(1)
        ns2 = ntrk(2)
C       Greater luminosoty than known -> linear 2D extrapolation
        if (lumi > luminosity(1, 1) .OR. lumi > luminosity(2, 1)) then
          call extrap1(lumi,color_U(1,1),color_U(1,2),luminosity(1,1),
     &         luminosity(1,2),c_1)
          call extrap1(lumi,color_U(2,1),color_U(2,2),luminosity(2,1),
     &         luminosity(2,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c1)
          if (c1 < 0.0) then
            c1 = 0.0
          end if
          call extrap1(lumi,color_B(1,1),color_B(1,2),luminosity(1,1),
     &         luminosity(1,2),c_1)
          call extrap1(lumi,color_B(2,1),color_B(2,2),luminosity(2,1),
     &         luminosity(2,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c2)
          if (c2 < 0.0) then
            c2 = 0.0
          end if
          call extrap1(lumi,color_V(1,1),color_V(1,2),luminosity(1,1),
     &         luminosity(1,2),c_1)
          call extrap1(lumi,color_V(2,1),color_V(2,2),luminosity(2,1),
     &         luminosity(2,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c3)
          if (c3 < 0.0) then
            c3 = 0.0
          end if
          call extrap1(lumi,color_R(1,1),color_R(1,2),luminosity(1,1),
     &         luminosity(1,2),c_1)
          call extrap1(lumi,color_R(2,1),color_R(2,2),luminosity(2,1),
     &         luminosity(2,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c4)
          if (c4 < 0.0) then 
            c4 = 0.0
          end if
          call extrap1(lumi,color_I(1,1),color_I(1,2),luminosity(1,1),
     &         luminosity(1,2),c_1)
          call extrap1(lumi,color_I(2,1),color_I(2,2),luminosity(2,1),
     &         luminosity(2,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c5)
          if (c5 < 0.0) then
            c5 = 0.0
          end if
          call extrap1(lumi,color_J(1,1),color_J(1,2),luminosity(1,1),
     &         luminosity(1,2),c_1)
          call extrap1(lumi,color_J(2,1),color_J(2,2),luminosity(2,1),
     &         luminosity(2,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c6)
          if (c6 < 0.0) then
            c6 = 0.0
          end if
          check3 = 1
          GOTO 45
C       Smaller luminosity than known -> linear 2D extrapolation
        else if (lumi < luminosity(1,ns1) 
     &           .or. lumi < luminosity(2,ns2)) then
          call extrap1(lumi,color_U(1,ns1-1),color_U(1,ns1),
     &         luminosity(1,ns1-1),luminosity(1,ns1),c_1)
          call extrap1(lumi,color_U(2,ns2-1),color_U(2,ns2),
     &         luminosity(2,ns2-1),luminosity(2,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c1)
          if (c1 < 0.0) then 
            c1 = 0.0
          end if
          call extrap1(lumi,color_B(1,ns1-1),color_B(1,ns1),
     &         luminosity(1,ns1-1),luminosity(1,ns1),c_1)
          call extrap1(lumi,color_B(2,ns2-1),color_B(2,ns2),
     &         luminosity(2,ns2-1),luminosity(2,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c2)
          if (c2 < 0.0) then
            c2 = 0.0
          end if
          call extrap1(lumi,color_V(1,ns1-1),color_V(1,ns1),
     &         luminosity(1,ns1-1),luminosity(1,ns1),c_1)
          call extrap1(lumi,color_V(2,ns2-1),color_V(2,ns2),
     &         luminosity(2,ns2-1),luminosity(2,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c3)
          if (c3 < 0.0) then
            c3 = 0.0
          end if
          call extrap1(lumi,color_R(1,ns1-1),color_R(1,ns1),
     &         luminosity(1,ns1-1),luminosity(1,ns1),c_1)
          call extrap1(lumi,color_R(2,ns2-1),color_R(2,ns2),
     &         luminosity(2,ns2-1),luminosity(2,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c4)
          if (c4 < 0.0) then 
            c4 = 0.0
          end if      
          call extrap1(lumi,color_I(1,ns1-1),color_I(1,ns1),
     &         luminosity(1,ns1-1),luminosity(1,ns1),c_1)
          call extrap1(lumi,color_I(2,ns2-1),color_I(2,ns2),
     &         luminosity(2,ns2-1),luminosity(2,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c5)
          if (c5 < 0.0) then 
            c5 = 0.0
          end if
          call extrap1(lumi,color_J(1,ns1-1),color_J(1,ns1),
     &         luminosity(1,ns1-1),luminosity(1,ns1),c_1)
          call extrap1(lumi,color_J(2,ns2-1),color_J(2,ns2),
     &         luminosity(2,ns2-1),luminosity(2,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c6)
          if (c6 < 0.0) then 
            c6 = 0.0
          end if
          check3 = 1
          GOTO 45
C       Luminosity between the known values
        else
          do i = 1, ns1 - 1
            if (lumi >= luminosity(1, i + 1) 
     &            .and. lumi <= luminosity(1, i)) then
              i1 = i
              check1 = 1
              GOTO 5
            end if
          end do
5         continue
          do i = 1, ns2 - 1
            if (lumi >= luminosity(2, i + 1) 
     &            .and. lumi <= luminosity(2, i)) then
              i2 = i
              check2 = 1
              GOTO 10
            end if
          end do
10        continue
          if (check1 == 1 .and. check2 == 1) then
            check3 = 1
            a1 = lumi - luminosity(1, i1)
            a2 = lumi - luminosity(2, i2)
            b1 = luminosity(1, i1 + 1) - luminosity(1, i1)
            b2 = luminosity(2, i2 + 1) - luminosity(2, i2)
            c_1 = color_U(1, i1) + (color_U(1, i1 + 1) 
     &            - color_U(1, i1)) * a1 / b1
            c_2 = color_U(2, i2) + (color_U(2, i2 + 1) 
     &            - color_U(2, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c1)
            c_1 = color_B(1, i1) + (color_B(1, i1 + 1) 
     &            - color_B(1, i1)) * a1 / b1
            c_2 = color_B(2, i2) + (color_B(2, i2 + 1) 
     &            - color_B(2, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c2)
            c_1 = color_V(1, i1) + (color_V(1, i1 + 1) 
     &            - color_V(1, i1)) * a1 / b1
            c_2 = color_V(2, i2) + (color_V(2, i2 + 1) 
     &            - color_V(2, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c3)
            c_1 = color_R(1, i1) + (color_R(1, i1 + 1) 
     &            - color_R(1, i1)) * a1 / b1
            c_2 = color_R(2, i2) + (color_R(2, i2 + 1) 
     &            - color_R(2, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c4)
            c_1 = color_I(1, i1) + (color_I(1, i1 + 1) 
     &            - color_I(1, i1)) * a1 / b1
            c_2 = color_I(2, i2) + (color_I(2, i2 + 1) 
     &            - color_I(2, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c5)
            c_1 = color_J(1, i1) + (color_J(1, i1 + 1) 
     &            - color_J(1, i1)) * a1 / b1
            c_2 = color_J(2, i2) + (color_J(2, i2 + 1) 
     &            - color_J(2, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c6)
            GOTO 45
          end if
        end if
      end if
      
C     Greater mass than known -> linear interpolation
      if (mass > mtrk(numberOfMassesWithColors)) then
        ns1 = ntrk(numberOfMassesWithColors - 1)
        ns2 = ntrk(numberOfMassesWithColors)
C       Greater luminosity than known -> linear 2D extrapolation
        if (lumi > luminosity(numberOfMassesWithColors - 1, 1) 
     &      .or. lumi > luminosity(numberOfMassesWithColors, 1)) then
          call extrap1(lumi,color_U(numberOfMassesWithColors - 1, 1),
     &         color_U(numberOfMassesWithColors - 1, 2),
     &         luminosity(numberOfMassesWithColors - 1, 1),
     &         luminosity(numberOfMassesWithColors - 1, 2), c_1)
          call extrap1(lumi,color_U(numberOfMassesWithColors, 1),
     &         color_U(numberOfMassesWithColors, 2),
     &         luminosity(numberOfMassesWithColors, 1),
     &         luminosity(numberOfMassesWithColors, 2), c_2)
          call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors - 1),
     &         mtrk(numberOfMassesWithColors),c1)
          if (c1 < 0.0) then 
            c1 = 0.0
          end if    
          call extrap1(lumi,color_B(numberOfMassesWithColors - 1, 1),
     &         color_B(numberOfMassesWithColors - 1, 2),
     &         luminosity(numberOfMassesWithColors - 1, 1),
     &         luminosity(numberOfMassesWithColors - 1, 2), c_1)
          call extrap1(lumi,color_B(numberOfMassesWithColors, 1),
     &         color_B(numberOfMassesWithColors, 2),
     &         luminosity(numberOfMassesWithColors, 1),
     &         luminosity(numberOfMassesWithColors, 2), c_2)
          call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors-1),
     &         mtrk(numberOfMassesWithColors),c2)
          if (c2 < 0.0) then 
            c2 = 0.0
          end if
          call extrap1(lumi,color_V(numberOfMassesWithColors-1,1),
     &         color_V(numberOfMassesWithColors-1,2),
     &         luminosity(numberOfMassesWithColors-1,1),
     &         luminosity(numberOfMassesWithColors-1,2),c_1)
          call extrap1(lumi,color_V(numberOfMassesWithColors,1),
     &         color_V(numberOfMassesWithColors,2),
     &         luminosity(numberOfMassesWithColors,1),
     &         luminosity(numberOfMassesWithColors,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors-1),
     &         mtrk(numberOfMassesWithColors),c3)
          if (c3 < 0.0) then 
            c3 = 0.0
          end if
          call extrap1(lumi,color_R(numberOfMassesWithColors-1,1),
     &         color_R(numberOfMassesWithColors-1,2),
     &         luminosity(numberOfMassesWithColors-1,1),
     &         luminosity(numberOfMassesWithColors-1,2),c_1)
          call extrap1(lumi,color_R(numberOfMassesWithColors,1),
     &         color_R(numberOfMassesWithColors,2),
     &         luminosity(numberOfMassesWithColors,1),
     &         luminosity(numberOfMassesWithColors,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors-1),
     &         mtrk(numberOfMassesWithColors),c4)
          if (c4 < 0.0) then
            c4 = 0.0
          end if
          call extrap1(lumi,color_I(numberOfMassesWithColors-1,1),
     &         color_I(numberOfMassesWithColors-1,2),
     &         luminosity(numberOfMassesWithColors-1,1),
     &         luminosity(numberOfMassesWithColors-1,2),c_1)
          call extrap1(lumi,color_I(numberOfMassesWithColors,1),
     &         color_I(numberOfMassesWithColors,2),
     &         luminosity(numberOfMassesWithColors,1),
     &         luminosity(numberOfMassesWithColors,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors-1),
     &         mtrk(numberOfMassesWithColors),c5)
          if (c5 < 0.0) then 
            c5 = 0.0
          end if
          call extrap1(lumi,color_J(numberOfMassesWithColors-1,1),
     &         color_J(numberOfMassesWithColors-1,2),
     &         luminosity(numberOfMassesWithColors-1,1),
     &         luminosity(numberOfMassesWithColors-1,2),c_1)
          call extrap1(lumi,color_J(numberOfMassesWithColors,1),
     &         color_J(numberOfMassesWithColors,2),
     &         luminosity(numberOfMassesWithColors,1),
     &         luminosity(numberOfMassesWithColors,2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors-1),
     &         mtrk(numberOfMassesWithColors),c6)
          if (c6 < 0.0) then 
            c6 = 0.0
          end if
          check3 = 1
          GOTO 45
C       Smaller luminosity than known -> linear 2D extrapolation
        else if (lumi < luminosity(numberOfMassesWithColors - 1, ns1)
     &           .OR. lumi < luminosity(numberOfMassesWithColors, ns1)) 
     &  then
          call extrap1(lumi,color_U(numberOfMassesWithColors-1,ns1-1),
     &         color_U(numberOfMassesWithColors-1,ns1),
     &         luminosity(numberOfMassesWithColors-1,ns1-1),
     &         luminosity(numberOfMassesWithColors-1,ns1),c_1)
          call extrap1(lumi,color_U(numberOfMassesWithColors,ns2-1),
     &         color_U(numberOfMassesWithColors,ns2),
     &        luminosity(numberOfMassesWithColors,ns2-1),
     &        luminosity(numberOfMassesWithColors,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c1)
          call extrap1(lumi,color_B(numberOfMassesWithColors-1,ns1-1),
     &         color_B(numberOfMassesWithColors-1,ns1),
     &         luminosity(numberOfMassesWithColors-1,ns2-1),
     &         luminosity(numberOfMassesWithColors-1,ns1),c_1)
          call extrap1(lumi,color_B(numberOfMassesWithColors,ns2-1),
     &         color_B(numberOfMassesWithColors,ns2),
     &         luminosity(numberOfMassesWithColors,ns2-1),
     &         luminosity(numberOfMassesWithColors,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c2)
          call extrap1(lumi,color_V(numberOfMassesWithColors-1,ns1-1),
     &         color_V(numberOfMassesWithColors-1,ns1),
     &         luminosity(numberOfMassesWithColors-1,ns1-1),
     &         luminosity(numberOfMassesWithColors-1,ns1),c_1)
          call extrap1(lumi,color_V(numberOfMassesWithColors,ns2-1),
     &         color_V(numberOfMassesWithColors,ns2),
     &         luminosity(numberOfMassesWithColors,ns2-1),
     &         luminosity(numberOfMassesWithColors,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c3)
          call extrap1(lumi,color_R(numberOfMassesWithColors-1,ns1-1),
     &         color_R(numberOfMassesWithColors-1,ns1),
     &         luminosity(numberOfMassesWithColors-1,ns1-1),
     &         luminosity(numberOfMassesWithColors-1,ns1),c_1)
          call extrap1(lumi,color_R(numberOfMassesWithColors,ns2-1),
     &         color_R(numberOfMassesWithColors,ns2),
     &         luminosity(numberOfMassesWithColors,ns2-1),
     &         luminosity(numberOfMassesWithColors,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c4)
          call extrap1(lumi,color_I(numberOfMassesWithColors-1,ns1-1),
     &         color_I(numberOfMassesWithColors-1,ns1),
     &         luminosity(numberOfMassesWithColors-1,ns1-1),
     &         luminosity(numberOfMassesWithColors-1,ns1),c_1)
          call extrap1(lumi,color_I(numberOfMassesWithColors,ns2-1),
     &         color_I(numberOfMassesWithColors,ns2),
     &         luminosity(numberOfMassesWithColors,ns2-1),
     &         luminosity(numberOfMassesWithColors,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c5)
          call extrap1(lumi,color_J(numberOfMassesWithColors-1,ns1-1),
     &         color_J(numberOfMassesWithColors-1,ns1),
     &         luminosity(numberOfMassesWithColors-1,ns1-1),
     &         luminosity(numberOfMassesWithColors-1,ns1),c_1)
          call extrap1(lumi,color_J(numberOfMassesWithColors,ns2-1),
     &         color_J(numberOfMassesWithColors,ns2),
     &         luminosity(numberOfMassesWithColors,ns2-1),
     &         luminosity(numberOfMassesWithColors,ns2),c_2)
          call extrap1(mass,c_1,c_2,mtrk(1),mtrk(2),c6)   
          check3 = 1
          GOTO 45
C       Luminosity between known values
        else
          do i = 1, ns1 - 1
            if (lumi >= luminosity(numberOfMassesWithColors - 1, i + 1)
     &          .and. lumi 
     &                <= luminosity(numberOfMassesWithColors - 1, i)) 
     &      then
              i1 = i
              check1 = 1
              GOTO 15
            end if
          end do
15        continue
          do i = 1, ns2 - 1
            if (lumi >= luminosity(numberOfMassesWithColors, i + 1) 
     &          .and. lumi <= luminosity(numberOfMassesWithColors, i)) 
     &      then
              i2 = i
              check2 = 1
              GOTO 20
            end if
          end do
20        continue
          if (check1 == 1 .and. check2 == 1) then
            check3 = 1
            a1 = lumi - luminosity(numberOfMassesWithColors - 1, i1)
            a2 = lumi - luminosity(numberOfMassesWithColors, i2)
            b1 = luminosity(numberOfMassesWithColors - 1, i1 + 1) 
     &           - luminosity(numberOfMassesWithColors - 1, i1)
            b2 = luminosity(numberOfMassesWithColors, i2 + 1)
     &           - luminosity(numberOfMassesWithColors, i2)
            c_1 = color_U(numberOfMassesWithColors - 1, i1)
     &            + (color_U(numberOfMassesWithColors - 1, i1 + 1)
     &               - color_U(numberOfMassesWithColors - 1, i1)) * a1 
     &              / b1
            c_2 = color_U(numberOfMassesWithColors, i2)
     &            + (color_U(numberOfMassesWithColors, i2 + 1)
     &               - color_U(numberOfMassesWithColors, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(1),
     &           mtrk(numberOfMassesWithColors),c1)
            c_1 = color_B(numberOfMassesWithColors - 1, i1)
     &            + (color_B(numberOfMassesWithColors - 1, i1 + 1)
     &               - color_B(numberOfMassesWithColors - 1, i1)) * a1 
     &              / b1
            c_2 = color_B(numberOfMassesWithColors, i2)
     &            + (color_B(numberOfMassesWithColors, i2 + 1)
     &               - color_B(numberOfMassesWithColors, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors-1),
     &           mtrk(numberOfMassesWithColors),c2)
            c_1 = color_V(numberOfMassesWithColors - 1, i1)
     &            + (color_V(numberOfMassesWithColors - 1, i1 + 1)
     &               - color_V(numberOfMassesWithColors - 1, i1)) * a1 
     &              / b1
            c_2 = color_V(numberOfMassesWithColors, i2) 
     &            + (color_V(numberOfMassesWithColors, i2 + 1)
     &               - color_V(numberOfMassesWithColors, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(1),
     &           mtrk(numberOfMassesWithColors),c3)
            c_1 = color_R(numberOfMassesWithColors - 1, i1)
     &            + (color_R(numberOfMassesWithColors - 1, i1 + 1)
     &               - color_R(numberOfMassesWithColors - 1, i1)) * a1 
     &              / b1
            c_2 = color_R(numberOfMassesWithColors, i2)
     &            + (color_R(numberOfMassesWithColors, i2 + 1)
     &               - color_R(numberOfMassesWithColors, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors-1),
     &           mtrk(numberOfMassesWithColors),c4)
            c_1 = color_I(numberOfMassesWithColors - 1, i1)
     &            + (color_I(numberOfMassesWithColors - 1, i1 + 1)
     &               - color_I(numberOfMassesWithColors - 1, i1)) * a1 
     &              / b1
            c_2 = color_I(numberOfMassesWithColors, i2)
     &            + (color_I(numberOfMassesWithColors, i2 + 1)
     &               - color_I(numberOfMassesWithColors, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors-1),
     &           mtrk(numberOfMassesWithColors),c5)
            c_1 = color_J(numberOfMassesWithColors - 1, i1)
     &            + (color_J(numberOfMassesWithColors - 1, i1 + 1)
     &               - color_J(numberOfMassesWithColors - 1, i1)) * a1 
     &              / b1
            c_2 = color_J(numberOfMassesWithColors, i2)
     &            + (color_J(numberOfMassesWithColors, i2 + 1)
     &               - color_J(numberOfMassesWithColors, i2)) * a2 / b2
            call extrap1(mass,c_1,c_2,mtrk(numberOfMassesWithColors-1),
     &           mtrk(numberOfMassesWithColors),c6)
            GOTO 45
          end if
        end if
      end if

C     Mass between known values -> linear interpolation
      do k = 1, numberOfMassesWithColors - 1
        if (mass > mtrk(k) .and. mass <= mtrk(k + 1)) then
          ns1 = ntrk(k)
          ns2 = ntrk(k + 1)
C         Larger luminosity than known -> linear 2D extrapolation
          if (lumi > luminosity(k, 1) 
     &        .or. lumi > luminosity(k + 1, 1)) then      
            call extrap1(lumi,color_U(k,1),color_U(k,2),luminosity(k,1),
     &           luminosity(k,2),c_1)
            call extrap1(lumi,color_U(k+1,1),color_U(k+1,2),
     &           luminosity(k+1,1),luminosity(k+1,2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c1)
            if (c1 < 0.0) then 
              c1=0.0
            end if        
            call extrap1(lumi,color_B(k,1),color_B(k,2),luminosity(k,1),
     &           luminosity(k,2),c_1)
            call extrap1(lumi,color_B(k+1,1),color_B(k+1,2),
     &           luminosity(k+1,1),luminosity(k+1,2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c2)
            if (c2 < 0.0) then 
              c2=0.0
            end if  
            call extrap1(lumi,color_V(k,1),color_V(k,2),luminosity(k,1),
     &           luminosity(k,2),c_1)
            call extrap1(lumi,color_V(k+1,1),color_V(k+1,2),
     &           luminosity(k+1,1),luminosity(k+1,2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c3)
            if (c3 < 0.0) then 
              c3=0.0
            end if  
            call extrap1(lumi,color_R(k,1),color_R(k,2),luminosity(k,1),
     &           luminosity(k,2),c_1)
            call extrap1(lumi,color_R(k+1,1),color_R(k+1,2),
     &           luminosity(k+1,1),luminosity(k+1,2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c4)
            if (c4 < 0.0) then 
              c4=0.0
            end if  
            call extrap1(lumi,color_I(k,1),color_I(k,2),luminosity(k,1),
     &           luminosity(k,2),c_1)
            call extrap1(lumi,color_I(k+1,1),color_I(k+1,2),
     &           luminosity(k+1,1),luminosity(k+1,2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c5)
            if (c5 < 0.0) then 
              c5=0.0
            end if
            call extrap1(lumi,color_J(k,1),color_J(k,2),luminosity(k,1),
     &           luminosity(k,2),c_1)
            call extrap1(lumi,color_J(k+1,1),color_J(k+1,2),
     &           luminosity(k+1,1),luminosity(k+1,2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c6)
            if (c6 < 0.0) then 
              c6=0.0
            end if 
            check3 = 1      
            GOTO 45
C         Smaller luminosity than known -> linear 2D extrapolation
          else if (lumi < luminosity(k, ns1) 
     &             .or. lumi < luminosity(k + 1, ns2)) then
            call extrap1(lumi,color_U(k,ns1-1),color_U(k,ns1),
     &           luminosity(k,ns1-1),luminosity(k,ns1),c_1)
            call extrap1(lumi,color_U(k+1,ns2-1),color_U(k+1,ns2),
     &           luminosity(k+1,ns2-1),luminosity(k+1,ns2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c1)
            call extrap1(lumi,color_B(k,ns1-1),color_B(k,ns1),
     &           luminosity(k,ns1-1),luminosity(k,ns1),c_1)
            call extrap1(lumi,color_B(k+1,ns2-1),color_B(k+1,ns2),
     &           luminosity(k+1,ns2-1),luminosity(k+1,ns2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c2)
            call extrap1(lumi,color_V(k,ns1-1),color_V(k,ns1),
     &          luminosity(k,ns1-1),luminosity(k,ns1),c_1)
            call extrap1(lumi,color_V(k+1,ns2-1),color_V(k+1,ns2),
     &           luminosity(k+1,ns2-1),luminosity(k+1,ns2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c3)
            call extrap1(lumi,color_R(k,ns1-1),color_R(k,ns1),
     &           luminosity(k,ns1-1),luminosity(k,ns1),c_1)
            call extrap1(lumi,color_R(k+1,ns2-1),color_R(k+1,ns2),
     &           luminosity(k+1,ns2-1),luminosity(k+1,ns2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c4)      
            call extrap1(lumi,color_I(k,ns1-1),color_I(k,ns1),
     &           luminosity(k,ns1-1),luminosity(k,ns1),c_1)
            call extrap1(lumi,color_I(k+1,ns2-1),color_I(k+1,ns2),
     &           luminosity(k+1,ns2-1),luminosity(k+1,ns2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c5)
            call extrap1(lumi,color_J(k,ns1-1),color_J(k,ns1),
     &           luminosity(k,ns1-1),luminosity(k,ns1),c_1)
            call extrap1(lumi,color_J(k+1,ns2-1),color_J(k+1,ns2),
     &           luminosity(k+1,ns2-1),luminosity(k+1,ns2),c_2)
            call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c6)  
            check3 = 1
            GOTO 45
C         Luminosity between known values
          else
            do i = 1, ns1 - 1
              if (lumi >= luminosity(k, i + 1) 
     &            .and. lumi <= luminosity(k, i)) 
     &        then
                i1 = i
                check1 = 1
                GOTO 25
              end if
            end do      
25          continue      
            do i = 1, ns2 - 1
              if (lumi >= luminosity(k + 1, i + 1)
     &            .and. lumi <= luminosity(k + 1, i)) then
                i2 = i
                check2 = 1
                GOTO 30
              end if
            end do
30          continue
            if (check1 == 1 .and. check2 == 1) then
              check3 = 1
              a1 = lumi - luminosity(k, i1)
              a2 = lumi - luminosity(k + 1, i2)
              b1 = luminosity(k,i1+1)-luminosity(k,i1)
              b2 = luminosity(k+1,i2+1)-luminosity(k+1,i2)
              c_1 = color_U(k,i1)+(color_U(k,i1+1)-color_U(k,i1))*a1/b1
              c_2 = color_U(k+1,i2)+(color_U(k+1,i2+1)-color_U(k+1,i2))*
     &            a2/b2
              call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c1)
              c_1 = color_B(k,i1)+(color_B(k,i1+1)-color_B(k,i1))*a1/b1
              c_2 = color_B(k+1,i2)+(color_B(k+1,i2+1)-color_B(k+1,i2))*
     &            a2/b2
             call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c2)
              c_1 = color_V(k,i1)+(color_V(k,i1+1)-color_V(k,i1))*a1/b1
              c_2 = color_V(k+1,i2)+(color_V(k+1,i2+1)-color_V(k+1,i2))*
     &            a2/b2
              call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c3)
              c_1 = color_R(k,i1)+(color_R(k,i1+1)-color_R(k,i1))*a1/b1
              c_2 = color_R(k+1,i2)+(color_R(k+1,i2+1)-color_R(k+1,i2))*
     &            a2/b2
              call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c4)
              c_1 = color_I(k,i1)+(color_I(k,i1+1)-color_I(k,i1))*a1/b1
              c_2 = color_I(k+1,i2)+(color_I(k+1,i2+1)-color_I(k+1,i2))*
     &            a2/b2
              call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c5)
              c_1 = color_J(k,i1)+(color_J(k,i1+1)-color_J(k,i1))*a1/b1
              c_2 = color_J(k+1,i2)+(color_J(k+1,i2+1)-color_J(k+1,i2))*
     &            a2/b2
              call extrap1(mass,c_1,c_2,mtrk(k),mtrk(k+1),c6)
              GOTO 45
            end if
          end if
        end if
      end do
45    continue

      if (check3 == 0) then
          write(1007, *) 'ERROR', lumi, mass
      end if
      end subroutine


C     TODO: find out the meaning of arguments
      subroutine extrap1(lumi, x1, x2, l1, l2, c)
          implicit none
          real :: lumi,
     &            x1,
     &            x2,
     &            l1,
     &            l2,
     &            c,
     &            s,
     &            b
      
          s = (x2 - x1) / (l2 - l1)
          b = x1 - s * l1
          c = s * lumi + b
      end subroutine
