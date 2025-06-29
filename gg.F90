!program write_to_file
   implicit none
   integer :: i
   integer, parameter :: unt=10
   open(unit = unt, file = 'output.txt', status='replace')
      do i = 1, 5
         write(unt, '(I4, 2X, F8.2)') i, i * 1.5
      end do
   close(unt)
   end program
!end program write_to_file
