

subroutine find_cycle(neis, Nneis, chain, chainlen, cycle, Ncycle, Newchain)
  ! use mt19937
  use mtmod

  implicit none

  integer, intent(IN) :: neis(:,:)
  integer, intent(IN) :: Nneis(:)
  integer, intent(INOUT) :: chain(:)
  integer, intent(INOUT) :: cycle(:)

  integer, intent(IN) :: chainlen ! points the last element of chain
  integer, intent(OUT) :: Ncycle, Newchain
  integer :: head, Nnexts, nexts(4), i, j, k, l, last, Nchain

  ! print *, neis(1,:)
  Nchain = chainlen
  head = chain(Nchain)
  ! print *, head, "head"
  if ( Nchain > 1 ) then
    last = chain(Nchain-1)
    ! print *, last, "last"
    Nnexts = 0
    do i=1, Nneis(head)
      j = neis(head, i)
      if ( j .ne. last ) then
        Nnexts = Nnexts + 1
        nexts(Nnexts) = j
      endif
    enddo
  else
    Nnexts = Nneis(head)
    nexts(:)  = neis(head, :)
  endif
  do
    i = int(grnd()*Nnexts) + 1
    ! print *, i, "random"
    ! print *, nexts, "nexts"
    head = nexts(i)
    ! print *, head, "new head"
    do k=1, Nchain
      if ( chain(k) .eq. head ) then
        ! return tail and cycle
        ! print *, k, "new head found at", chain
        Newchain = k-1
        do l=0, Nchain-k
          cycle(l+1) = chain(l+k)
        enddo
        Ncycle = Nchain-k+1
        return
      endif
    enddo
    Nchain = Nchain + 1
    chain(Nchain) = head
    last = chain(Nchain-1)
    Nnexts = 0
    do i=1, Nneis(head)
      j = neis(head, i)
      if ( j .ne. last ) then
        Nnexts = Nnexts + 1
        nexts(Nnexts) = j
      endif
    enddo
  enddo
end subroutine find_cycle


subroutine remove_edge(neis, Nneis, a, b)
  implicit none

  integer, intent(INOUT) :: neis(:,:)
  integer, intent(INOUT) :: Nneis(:)
  integer, intent(IN) :: a, b
  integer :: i,j

  do i=1, Nneis(a)
    j = neis(a,i)
    if (j .eq. b) then
      neis(a,i) = neis(a,Nneis(a))
      Nneis(a) = Nneis(a) - 1
      return
    endif
  enddo
end subroutine remove_edge



subroutine remove_edge2(neis, Nneis, b)
  implicit none

  integer, intent(INOUT) :: neis(4)
  integer, intent(INOUT) :: Nneis
  integer, intent(IN) :: b
  integer :: i,j

  do i=1, Nneis
    j = neis(i)
    if (j .eq. b) then
      neis(i) = neis(Nneis)
      Nneis = Nneis - 1
      return
    endif
  enddo
end subroutine remove_edge2



subroutine remove_cycle(neis, Nneis, cycle, Ncycle)
  implicit none

  integer, intent(INOUT) :: neis(:,:)
  integer, intent(INOUT) :: Nneis(:)
  integer, intent(IN) :: cycle(:)
  integer, intent(IN) :: Ncycle
  integer :: i,j,a,b, k,l ! head, Nnexts, nexts(4), i, j, k, l, last, Nchain

  do i=1, Ncycle
    j = i+1
    if ( j > Ncycle ) then
      j = 1
    endif

    a = cycle(i)
    b = cycle(j)

    do k=1, Nneis(a)
      l = neis(a,k)
      if (l .eq. b) then
        neis(a,k) = neis(a,Nneis(a))
        Nneis(a) = Nneis(a) - 1
        exit
      endif
    enddo
    do k=1, Nneis(b)
      l = neis(b,k)
      if (l .eq. a) then
        neis(b,k) = neis(b,Nneis(b))
        Nneis(b) = Nneis(b) - 1
        exit
      endif
    enddo

    ! call remove_edge2(neis(a,:), Nneis(a), b)
    ! call remove_edge2(neis(b,:), Nneis(b), a)
    ! call remove_edge(neis, Nneis, a,b)
    ! call remove_edge(neis, Nneis, b,a)
  enddo
end subroutine remove_cycle



! subroutine tileByCycles(neis, Nneis, cycles, Ncycles)
!   implicit none
!   integer, intent(INOUT) :: neis(:,:), Nneis(:)
!   integer, intent(INOUT) :: cycles

  ! 長さのちがう配列を束ねたものを作るのがとても面倒。
  ! allocatableな配列で返して、pythonがわでdeallocate
  ! できないんかな。

! def tileByCycles(g):
!     """
!     Tile the graph with cycles.
!     g is a graph defined as a list of sets.
!     g is destroyed by the algorithm.
!     Returns the list of cycles
!     """
!     cycles = []
!     chain = []
!     nc = 0
!     tick = 1
!     N = len(g)*2
!     while len(g) > 0:
!         if len(chain) == 0:
!             # prepare a new chain
!             L = list(g)
!             head = random.choice(L)
!             chain = [head]
!         # Randomly find a cycle
!         chain, cycle = find_cycle(g, chain)
!         cycles.append(cycle)
!         nc += len(cycle)
!         if tick*N < nc*10:
!             logger.info(f"* {tick}/10 tiled.")
!             tick += 1
!         for a,b in cycle_edges(cycle):
!             # remove edges in the cycle
!             g[a].remove(b)
!             g[b].remove(a)
!             # remove nodes also
!             if len(g[a]) == 0:
!                 del g[a]
!             if len(g[b]) == 0:
!                 del g[b]
!     return cycles
