<script>
  import '../app.pcss';
  import { AppShell } from '@skeletonlabs/skeleton';
  import { LightSwitch } from '@skeletonlabs/skeleton';

  import DocumentIcon from '../components/assets/DocumentIcon.svelte';
  import DocumentChecklistIcon from '../components/assets/DocumentCheckListIcon.svelte';
  import ChartIcon from '../components/assets/ChartIcon.svelte';
  import BriefCaseIcon from '../components/assets/BriefCaseIcon.svelte';
  import RocketIcon from '../components/assets/RocketIcon.svelte';
  import HomeIcon from '../components/assets/HomeIcon.svelte';
  import BugIcon from '../components/assets/BugIcon.svelte';
  import BookmarkIcon from '../components/assets/BookmarkIcon.svelte'
</script>

<AppShell slotSidebarLeft="bg-surface-500/5 w-10 p-0 lg:w-64">
  <svelte:fragment slot="sidebarLeft">
    <!-- User Profile -->
    <a class="user-profile-img-link flex flex-row items-center" href="/me">
      <div class="placeholder-test w-10 m-2 placeholder-circle"></div>
      <div class="user-name">
        <span class="span">username</span>
      </div>
    </a>

    <!-- Navbar -->
    <hr />
    <nav class="list-nav">
      <ul>
        <li>
          <a href="/projects">
            <BookmarkIcon />
            <div class="list-nav-bar-item-title">Projects</div>
          </a>
        </li>
        <li>
          <a href="/">
            <HomeIcon />
            <div class="list-nav-bar-item-title">Dashboard</div>
          </a>
        </li>
        <li>
          <a href="/suites">
            <BriefCaseIcon />
            <div class="list-nav-bar-item-title">Suites</div>
          </a>
        </li>
        <li>
          <a href="/suites/test-cases">
            <DocumentIcon />

            <div class="list-nav-bar-item-title">Test Cases</div>
          </a>
        </li>
        <li>
          <a href="/suites/checklists">
            <DocumentChecklistIcon />
            <div class="list-nav-bar-item-title">Checklists</div>
          </a>
        </li>
        <li>
          <a href="/test-runs">
            <RocketIcon />
            <div class="list-nav-bar-item-title">Test Runs</div>
          </a>
        </li>
        <li>
          <a href="/bug-reports">
            <BugIcon />
            <div class="list-nav-bar-item-title">Bug Reports</div>
          </a>
        </li>
        <li>
          <a href="/review">
            <ChartIcon />
            <div class="list-nav-bar-item-title">Review</div>
          </a>
        </li>
      </ul>
    </nav>
    <LightSwitch class="absolute bottom-2 left-2 hidden lg:block" />
  </svelte:fragment>
  <slot />
</AppShell>

<style>
</style>
