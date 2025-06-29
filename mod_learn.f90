module mod_learn

    ! provides precision for data types
    use iso_fortran_env

    ! artifact of legacy code
    implicit none

contains

    function basics()
        ! ***** initialize data types
        real(real64) :: a, b
        integer(int64) :: i, j
        complex(real64) :: c
        logical :: basics
        character(len=12) :: msg

        a = 0
        b = 3
        i = 4
        j = 5
        c = (1,2)
        basics = .true.
        msg = "hello world!"

        print *, "floats", a, b
        print *, "ints", i, j
        print *, "complex",c, c%re, c%im
        print *, "bools", basics
        print *, msg
        ! ***** initialize data types

    end function basics

end module

program main
    use mod_learn, only : basics
    implicit none
    logical :: flag
    flag = basics()
    print *, flag

end program 